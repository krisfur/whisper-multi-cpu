# Whisper Parallel CPU Audio & Video Transcriber

A minimal, robust Python package for whisper.cpp with CPU-optimized threading and integrated model management. Transcribe both audio and video files with high performance. Targeting distributed cloud deployments and transcription workflows.

## 🚀 Quick Start

**Install from PyPI:**
```bash
pip install whisper-parallel-cpu
```

**Use in Python:**
```python
import whisper_parallel_cpu

# Transcribe audio files
text = whisper_parallel_cpu.transcribe("audio.mp3", model="base")

# Transcribe video files
text = whisper_parallel_cpu.transcribe("video.mp4", model="base")

# Or use specific functions
text = whisper_parallel_cpu.transcribe_audio("audio.wav", model="small")
text = whisper_parallel_cpu.transcribe_video("video.mkv", model="medium")
```

**Or use the CLI:**
```bash
# Transcribe audio
whisper_parallel_cpu transcribe audio.mp3 --model base

# Transcribe video
whisper_parallel_cpu transcribe video.mp4 --model base
```

---

## ✨ Features

- **Native C++/pybind11 speed** (CPU & GPU acceleration)
- **Automatic model download/caching** - no manual setup required
- **Simple Python & CLI interface** - just `pip install` and go
- **Input**: Audio (`.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`) and video (`.mp4`, `.mkv`, `.avi`, `.mov`) formats
- **Output**: Transcribed text as a Python string
- **Benchmarking**: Built-in performance testing and optimization tools
- **Cross-platform**: Works on macOS, Linux, and Windows

---

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install whisper-parallel-cpu
```

### From Source (Development)
```bash
# Clone the repository
git clone https://github.com/krisfur/whisper-parallel-cpu.git
cd whisper-parallel-cpu

# Install in editable mode
pip install -e .

# Test the installation
python test_transcribe.py video.mp4
```

---

## 🧰 Requirements

### System Tools
- **C++17 compiler** (`g++`, `clang++`) - automatically handled by pip
- **cmake** (>=3.15) - automatically handled by pip
- **ffmpeg** (for audio extraction)

### Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Chocolatey:
```bash
choco install ffmpeg
```

---

## 🧪 Usage

### Python API

#### Basic Usage (Function-based)

```python
import whisper_parallel_cpu

# Transcribe any audio or video file (auto-detects format)
text = whisper_parallel_cpu.transcribe("audio.mp3", model="base", threads=4)
text = whisper_parallel_cpu.transcribe("video.mp4", model="small")

# Use specific functions for audio or video
text = whisper_parallel_cpu.transcribe_audio("audio.wav", model="base", threads=4)
text = whisper_parallel_cpu.transcribe_video("video.mkv", model="medium", threads=8)

# CPU-only mode (no GPU)
text = whisper_parallel_cpu.transcribe("audio.flac", model="base", use_gpu=False)
```

#### Advanced Usage (Model Reuse)

For better performance when transcribing multiple files, use the `WhisperModel` class to load the model once and reuse it:

```python
from whisper_parallel_cpu import WhisperModel

# Create a model instance (model is loaded on first use)
model = WhisperModel(model="base", use_gpu=False, threads=4)

# Transcribe multiple files using the same loaded model
files = ["audio1.mp3", "audio2.wav", "video1.mp4", "video2.mkv"]
for file_path in files:
    text = model.transcribe(file_path)
    print(f"Transcribed {file_path}: {text[:100]}...")

# Use as context manager
with WhisperModel(model="small", use_gpu=True) as model:
    text1 = model.transcribe("audio1.mp3")
    text2 = model.transcribe("audio2.wav")
    # Model is automatically managed

# Memory management
model.clear_contexts()  # Free memory
print(f"Active contexts: {model.get_context_count()}")
```

### Supported File Formats

**Audio Formats:**
- `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, `.wma`, `.opus`, `.webm`, `.3gp`, `.amr`, `.au`, `.ra`, `.mid`, `.midi`

**Video Formats:**
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.3gp`, `.ogv`, `.ts`, `.mts`, `.m2ts`

### Available Models

The following models are available and will be downloaded automatically:

| Model | Size | Accuracy | Speed | Use Case |
|-------|------|----------|-------|----------|
| `tiny` | 74MB | Good | Fastest | Quick transcriptions |
| `base` | 141MB | Better | Fast | General purpose |
| `small` | 444MB | Better | Medium | High accuracy needed |
| `medium` | 1.4GB | Best | Slow | Maximum accuracy |
| `large` | 2.9GB | Best | Slowest | Professional use |

### Command Line Interface

```bash
# List available models
whisper_parallel_cpu list

# Download a specific model
whisper_parallel_cpu download base

# Transcribe audio files
whisper_parallel_cpu transcribe audio.mp3 --model base --threads 4
whisper_parallel_cpu transcribe audio.wav --model small

# Transcribe video files
whisper_parallel_cpu transcribe video.mp4 --model base --threads 4
whisper_parallel_cpu transcribe video.mkv --model medium

# Transcribe without GPU (CPU-only)
whisper_parallel_cpu transcribe audio.flac --model small --no-gpu
```

### Model Management

```python
import whisper_parallel_cpu

# List available models
whisper_parallel_cpu.list_models()

# Download a specific model
whisper_parallel_cpu.download_model("medium")

# Force re-download
whisper_parallel_cpu.download_model("base", force=True)
```

---

## 🔧 Troubleshooting

### Common Issues

#### Import Error: `libwhisper.so.1: cannot open shared object file`

This error occurs on Linux when the package's native extensions can't find the required shared libraries. This is typically resolved by:

1. **Installing from source** (recommended):
   ```bash
   pip install --no-binary=whisper-parallel-cpu whisper-parallel-cpu
   ```

2. **Installing system dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install -y ffmpeg cmake build-essential
   
   # CentOS/RHEL
   sudo yum install -y ffmpeg cmake gcc-c++
   ```

3. **Building from source**:
   ```bash
   git clone https://github.com/krisfur/whisper-parallel-cpu.git
   cd whisper-parallel-cpu
   pip install -e .
   ```

#### Build Failures

If you encounter build failures:

1. **Ensure you have the required system dependencies**:
   - C++17 compiler (gcc/g++ or clang)
   - cmake >= 3.15
   - ffmpeg

2. **Check your Python version**: The package requires Python 3.8+

3. **Try building with verbose output**:
   ```bash
   pip install --verbose --no-binary=whisper-parallel-cpu whisper-parallel-cpu
   ```

#### Runtime Issues

- **Memory errors**: Use smaller models (`tiny`, `base`) or reduce thread count
- **Slow performance**: Use GPU acceleration if available, or optimize thread count
- **Audio extraction failures**: Ensure ffmpeg is properly installed and accessible

### Testing Your Installation

Run the test script to verify your installation:

```bash
python test_build.py
```

This will test both the import and basic functionality of the package.

---

## 📊 Benchmarking & Performance

### Run Performance Tests

```bash
# Test with 5 audio/video copies
python benchmark.py audio.mp3 5
python benchmark.py video.mp4 5
```

### What the Benchmark Tests

1. **Thread Scaling**: Tests different thread counts (1, 2, 4, 8, 16, etc.) for single audio/video transcription
2. **Sequential Processing**: Measures throughput when processing multiple audio/video files one after another
3. **Parallel Processing**: Tests concurrent processing with different numbers of workers
4. **Optimal Configuration**: Provides the best settings for your specific hardware

### Performance Optimization Tips

1. **Model Reuse**: Use `WhisperModel` class for multiple transcriptions to avoid reloading the model each time
2. **GPU Acceleration**: The system automatically uses Metal (macOS) or CUDA (Linux/Windows) when available
3. **Thread Count**: Use the benchmark to find optimal thread count for your CPU
4. **Batch Processing**: For multiple audio/video files, use parallel processing with ThreadPoolExecutor
5. **Model Size**: Smaller models (base, small) are faster but less accurate than larger ones (medium, large)

### Model Reuse Performance

When transcribing multiple files, using the `WhisperModel` class can provide significant performance improvements:

```python
from whisper_parallel_cpu import WhisperModel
import time

# Method 1: Using WhisperModel (model reuse) - FASTER
model = WhisperModel(model="base")
start = time.time()
for file in files:
    text = model.transcribe(file)
model_time = time.time() - start

# Method 2: Using transcribe function (no reuse) - SLOWER
start = time.time()
for file in files:
    text = whisper_parallel_cpu.transcribe(file, model="base")
function_time = time.time() - start

print(f"Speedup with model reuse: {function_time / model_time:.2f}x")
```

**Typical speedups:**
- 2-5x faster for multiple files with the same model
- Reduced memory usage through context sharing
- Better for batch processing workflows

---

## ⚙️ API Reference

### `transcribe(file_path, model, threads, use_gpu)`

Transcribes an audio or video file using Whisper. Automatically detects file type.

**Parameters:**
- `file_path` (str): Path to the audio or video file
- `model` (str): Model name (e.g. "base", "tiny", etc.) or path to Whisper model binary (.bin file)
- `threads` (int): Number of CPU threads to use (default: 4)
- `use_gpu` (bool): Whether to use GPU acceleration (default: True)

**Returns:**
- `str`: Transcribed text

### `transcribe_audio(audio_path, model, threads, use_gpu)`

Transcribes an audio file using Whisper.

**Parameters:**
- `audio_path` (str): Path to the audio file
- `model` (str): Model name (e.g. "base", "tiny", etc.) or path to Whisper model binary (.bin file)
- `threads` (int): Number of CPU threads to use (default: 4)
- `use_gpu` (bool): Whether to use GPU acceleration (default: True)

**Returns:**
- `str`: Transcribed text

### `transcribe_video(video_path, model, threads, use_gpu)`

Transcribes a video file using Whisper.

**Parameters:**
- `video_path` (str): Path to the video file
- `model` (str): Model name (e.g. "base", "tiny", etc.) or path to Whisper model binary (.bin file)
- `threads` (int): Number of CPU threads to use (default: 4)
- `use_gpu` (bool): Whether to use GPU acceleration (default: True)

**Returns:**
- `str`: Transcribed text

**Example:**
```python
import whisper_parallel_cpu

# Basic usage
text = whisper_parallel_cpu.transcribe_video("sample.mp4")

# Advanced usage
text = whisper_parallel_cpu.transcribe_video(
    "sample.mp4", 
    model="medium", 
    threads=8, 
    use_gpu=False
)
```

### `WhisperModel(model, use_gpu, threads)`

A class for efficient model reuse across multiple transcriptions.

**Parameters:**
- `model` (str): Model name (e.g. "base", "tiny", etc.) or path to Whisper model binary (.bin file)
- `use_gpu` (bool): Whether to use GPU acceleration (default: False)
- `threads` (int): Number of CPU threads to use (default: 4)

**Methods:**
- `transcribe(file_path)`: Transcribe any audio or video file
- `transcribe_audio(audio_path)`: Transcribe an audio file
- `transcribe_video(video_path)`: Transcribe a video file
- `clear_contexts()`: Clear all cached contexts to free memory
- `get_context_count()`: Get number of cached contexts

**Example:**
```python
from whisper_parallel_cpu import WhisperModel

# Create model instance
model = WhisperModel(model="base", use_gpu=False, threads=4)

# Transcribe multiple files efficiently
files = ["audio1.mp3", "audio2.wav", "video1.mp4"]
for file_path in files:
    text = model.transcribe(file_path)
    print(f"Transcribed: {text[:50]}...")

# Memory management
model.clear_contexts()
```

### `clear_contexts()`

Clear all cached whisper contexts to free memory.

**Example:**
```python
import whisper_parallel_cpu

# Clear all cached contexts
whisper_parallel_cpu.clear_contexts()
```

### `get_context_count()`

Get the number of currently cached whisper contexts.

**Returns:**
- `int`: Number of cached contexts

**Example:**
```python
import whisper_parallel_cpu

# Check how many contexts are cached
count = whisper_parallel_cpu.get_context_count()
print(f"Active contexts: {count}")
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on [whisper.cpp](https://github.com/ggerganov/whisper.cpp) by Georgi Gerganov
- Uses [pybind11](https://github.com/pybind/pybind11) for Python bindings
- Model management inspired by the original OpenAI Whisper project
