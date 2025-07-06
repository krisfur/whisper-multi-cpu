# Whisper Parallel CPU Video Transcriber

A minimal, robust Python package for whisper.cpp with CPU-optimized threading and integrated model management. Targeting distributed cloud deployments and transcription of video files.

## 🚀 Quick Start

**Install from PyPI:**
```bash
pip install whisper-parallel-cpu
```

**Use in Python:**
```python
import whisper_parallel_cpu
text = whisper_parallel_cpu.transcribe("video.mp4", model="base")
```

**Or use the CLI:**
```bash
whisper_parallel_cpu transcribe video.mp4 --model base
```

---

## ✨ Features

- **Native C++/pybind11 speed** (CPU & GPU acceleration)
- **Automatic model download/caching** - no manual setup required
- **Simple Python & CLI interface** - just `pip install` and go
- **Input**: `.mp4`, `.mkv`, or any video format `ffmpeg` supports
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

```python
import whisper_parallel_cpu

# Transcribe with automatic model downloading
text = whisper_parallel_cpu.transcribe_video("video.mp4", model="base", threads=4)
print(text)

# Or use the shorter alias
text = whisper_parallel_cpu.transcribe("video.mp4", model="small")
print(text)

# CPU-only mode (no GPU)
text = whisper_parallel_cpu.transcribe("video.mp4", model="base", use_gpu=False)
```

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

# Transcribe a video
whisper_parallel_cpu transcribe video.mp4 --model base --threads 4

# Transcribe without GPU (CPU-only)
whisper_parallel_cpu transcribe video.mp4 --model small --no-gpu
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

## 📊 Benchmarking & Performance

### Run Performance Tests

```bash
# Test with 5 video copies
python benchmark.py video.mp4 5
```

### What the Benchmark Tests

1. **Thread Scaling**: Tests different thread counts (1, 2, 4, 8, 16, etc.) for single video transcription
2. **Sequential Processing**: Measures throughput when processing multiple videos one after another
3. **Parallel Processing**: Tests concurrent processing with different numbers of workers
4. **Optimal Configuration**: Provides the best settings for your specific hardware

### Performance Optimization Tips

1. **GPU Acceleration**: The system automatically uses Metal (macOS) or CUDA (Linux/Windows) when available
2. **Thread Count**: Use the benchmark to find optimal thread count for your CPU
3. **Batch Processing**: For multiple videos, use parallel processing with ThreadPoolExecutor
4. **Model Size**: Smaller models (base, small) are faster but less accurate than larger ones (medium, large)

---

## ⚙️ API Reference

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
