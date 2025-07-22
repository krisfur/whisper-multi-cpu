// bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// Forward declarations from transcriber.cpp
std::string transcribe_video(const std::string& video_path,
                             const std::string& model,
                             int threads,
                             bool use_gpu);

std::string transcribe_video_legacy(const std::string& video_path,
                                    const std::string& model,
                                    int threads,
                                    bool use_gpu);

void clear_whisper_contexts();
size_t get_whisper_context_count();

namespace py = pybind11;

PYBIND11_MODULE(whisper_parallel_cpu, m) {
    m.def("transcribe_video", &transcribe_video,
          py::arg("video_path"),
          py::arg("model") = "models/ggml-base.en.bin",
          py::arg("threads") = 4,
          py::arg("use_gpu") = true,
          "Transcribe a video using whisper.cpp with C++ backend and context reuse.");
    
    m.def("transcribe_video_legacy", &transcribe_video_legacy,
          py::arg("video_path"),
          py::arg("model") = "models/ggml-base.en.bin",
          py::arg("threads") = 4,
          py::arg("use_gpu") = true,
          "Transcribe a video using whisper.cpp with C++ backend (legacy mode, no context reuse).");
    
    m.def("clear_whisper_contexts", &clear_whisper_contexts,
          "Clear all cached whisper contexts to free memory.");
    
    m.def("get_whisper_context_count", &get_whisper_context_count,
          "Get the number of currently cached whisper contexts.");
}