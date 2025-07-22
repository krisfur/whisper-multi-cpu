// transcriber.cpp
#include <cstdlib>
#include <string>
#include <sstream>
#include <thread>
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <memory>
#include <unordered_map>
#include <mutex>

// Include whisper.cpp headers
#include "whisper.h"
#include "common.h"
#include "common-whisper.h"

namespace fs = std::filesystem;

// Global context manager for reusing whisper contexts
class WhisperContextManager {
private:
    std::unordered_map<std::string, std::unique_ptr<whisper_context, decltype(&whisper_free)>> contexts_;
    std::mutex contexts_mutex_;
    
public:
    whisper_context* get_context(const std::string& model_path, bool use_gpu) {
        std::lock_guard<std::mutex> lock(contexts_mutex_);
        
        // Create a unique key for this model + GPU setting
        std::string key = model_path + "_" + (use_gpu ? "gpu" : "cpu");
        
        auto it = contexts_.find(key);
        if (it != contexts_.end()) {
            return it->second.get();
        }
        
        // Initialize new context
        struct whisper_context_params cparams = whisper_context_default_params();
        cparams.use_gpu = use_gpu;
        whisper_context* ctx = whisper_init_from_file_with_params(model_path.c_str(), cparams);
        if (ctx == nullptr) {
            throw std::runtime_error("Failed to initialize whisper context from model: " + model_path);
        }
        
        contexts_.emplace(key, std::unique_ptr<whisper_context, decltype(&whisper_free)>(ctx, &whisper_free));
        return ctx;
    }
    
    void clear_contexts() {
        std::lock_guard<std::mutex> lock(contexts_mutex_);
        contexts_.clear();
    }
    
    size_t get_context_count() {
        std::lock_guard<std::mutex> lock(contexts_mutex_);
        return contexts_.size();
    }
};

// Global instance
static WhisperContextManager g_context_manager;

// Run ffmpeg to extract mono 16kHz audio
bool extract_audio(const std::string& input_video, const std::string& output_wav) {
    std::stringstream cmd;
    cmd << "ffmpeg -y -i \"" << input_video << "\""
        << " -ar 16000 -ac 1 -f wav \"" << output_wav << "\""
        << " -loglevel error";
    return std::system(cmd.str().c_str()) == 0;
}

// Load audio file using whisper.cpp's common utilities
std::vector<float> load_audio(const std::string& wav_path) {
    std::vector<float> pcmf32;
    std::vector<std::vector<float>> pcmf32s;
    if (!read_audio_data(wav_path, pcmf32, pcmf32s, false)) {
        throw std::runtime_error("Failed to read WAV file: " + wav_path);
    }
    return pcmf32;
}

// Transcribe audio using whisper.cpp library directly with context reuse
std::string whisper_transcribe(const std::vector<float>& pcmf32,
                               int threads,
                               const std::string& model_path,
                               bool use_gpu = true) {
    // Get or create whisper context
    whisper_context* ctx = g_context_manager.get_context(model_path, use_gpu);

    // Initialize whisper parameters
    whisper_full_params params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    params.print_progress = false;
    params.print_special = false;
    params.print_timestamps = false;
    params.print_realtime = false;
    params.translate = false;
    params.language = "auto";
    params.detect_language = false;
    params.n_threads = threads;
    params.offset_ms = 0;
    params.no_context = true;
    params.single_segment = true;
    params.no_timestamps = true;

    // Run whisper
    if (whisper_full(ctx, params, pcmf32.data(), pcmf32.size()) != 0) {
        throw std::runtime_error("Failed to run whisper transcription");
    }

    // Get the result
    const int n_segments = whisper_full_n_segments(ctx);
    std::string result;
    for (int i = 0; i < n_segments; ++i) {
        const char* text = whisper_full_get_segment_text(ctx, i);
        if (text) {
            result += text;
            if (i < n_segments - 1) {
                result += " ";
            }
        }
    }
    return result;
}

// Legacy function that creates a new context each time (for backward compatibility)
std::string whisper_transcribe_legacy(const std::vector<float>& pcmf32,
                                      int threads,
                                      const std::string& model_path,
                                      bool use_gpu = true) {
    // Initialize whisper context
    struct whisper_context_params cparams = whisper_context_default_params();
    cparams.use_gpu = use_gpu;  // Set GPU usage
    struct whisper_context* ctx = whisper_init_from_file_with_params(model_path.c_str(), cparams);
    if (ctx == nullptr) {
        throw std::runtime_error("Failed to initialize whisper context from model: " + model_path);
    }
    // Clean up context when function exits
    std::unique_ptr<whisper_context, decltype(&whisper_free)> ctx_guard(ctx, whisper_free);

    // Initialize whisper parameters
    whisper_full_params params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    params.print_progress = false;
    params.print_special = false;
    params.print_timestamps = false;
    params.print_realtime = false;
    params.translate = false;
    params.language = "auto";
    params.detect_language = false;
    params.n_threads = threads;
    params.offset_ms = 0;
    params.no_context = true;
    params.single_segment = true;
    params.no_timestamps = true;

    // Run whisper
    if (whisper_full(ctx, params, pcmf32.data(), pcmf32.size()) != 0) {
        throw std::runtime_error("Failed to run whisper transcription");
    }

    // Get the result
    const int n_segments = whisper_full_n_segments(ctx);
    std::string result;
    for (int i = 0; i < n_segments; ++i) {
        const char* text = whisper_full_get_segment_text(ctx, i);
        if (text) {
            result += text;
            if (i < n_segments - 1) {
                result += " ";
            }
        }
    }
    return result;
}

// Entry function with context reuse
std::string transcribe_video(const std::string& video_path,
                             const std::string& model,
                             int threads,
                             bool use_gpu = true) {
    fs::path tmp_wav = fs::temp_directory_path() / "whisper_parallel_cpu_tmp.wav";

    if (!extract_audio(video_path, tmp_wav.string())) {
        throw std::runtime_error("Failed to extract audio with ffmpeg");
    }

    try {
        // Load audio
        std::vector<float> pcmf32 = load_audio(tmp_wav.string());
        // Transcribe with context reuse
        std::string result = whisper_transcribe(pcmf32, threads, model, use_gpu);
        // Clean up temp file
        fs::remove(tmp_wav);
        return result;
    } catch (const std::exception& e) {
        // Clean up temp file even if transcription fails
        fs::remove(tmp_wav);
        throw;
    }
}

// Legacy entry function (for backward compatibility)
std::string transcribe_video_legacy(const std::string& video_path,
                                    const std::string& model,
                                    int threads,
                                    bool use_gpu = true) {
    fs::path tmp_wav = fs::temp_directory_path() / "whisper_parallel_cpu_tmp.wav";

    if (!extract_audio(video_path, tmp_wav.string())) {
        throw std::runtime_error("Failed to extract audio with ffmpeg");
    }

    try {
        // Load audio
        std::vector<float> pcmf32 = load_audio(tmp_wav.string());
        // Transcribe with legacy approach
        std::string result = whisper_transcribe_legacy(pcmf32, threads, model, use_gpu);
        // Clean up temp file
        fs::remove(tmp_wav);
        return result;
    } catch (const std::exception& e) {
        // Clean up temp file even if transcription fails
        fs::remove(tmp_wav);
        throw;
    }
}

// Context management functions
void clear_whisper_contexts() {
    g_context_manager.clear_contexts();
}

size_t get_whisper_context_count() {
    return g_context_manager.get_context_count();
}