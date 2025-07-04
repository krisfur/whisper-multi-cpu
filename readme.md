# WhisperCPP Video Transcriber

High-performance video transcription for Python, powered by whisper.cpp (C++ backend).
**No manual model downloads or C++ setup required.**

---

## 🔧 Quick Install & Usage

```bash
# 1. Install system dependencies (ffmpeg, cmake, C++17 compiler)
# 2. Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -e .  # or pip install whispercpp if on PyPI
```

**Transcribe a video in Python:**
```python
import whispercpp
text = whispercpp.transcribe("video.mp4", model="base")
print(text)
```

**Or from the command line:**
```bash
whispercpp transcribe video.mp4 --model base
```

> The required model will be downloaded automatically on first use.

---

## 🚀 Features

- Native C++/pybind11 speed (CPU & GPU)
- Automatic model download/caching
- Simple Python & CLI interface
- No manual C++ or model setup
- Input: `.mp4`, `.mkv`, or any video format `ffmpeg` supports
- Output: Transcribed text as a Python string
- Benchmarking: Built-in performance testing and optimization tools

---

## 🧰 Requirements

### System Tools

- C++17 compiler (`g++`, `clang++`)
- `cmake` (>=3.15)
- `ffmpeg` (for audio extraction)

### Python

```bash
pip install pybind11 psutil
```

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

## 🧪 Usage Details

### Python API

```python
import whispercpp

# Transcribe with automatic model downloading
text = whispercpp.transcribe_video("video.mp4", model="base", threads=4)
print(text)

# Or use the shorter alias
text = whispercpp.transcribe("video.mp4", model="small")
print(text)
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

The package includes a CLI for easy model management and transcription:

```bash
# List available models
whispercpp list

# Download a specific model
whispercpp download base

# Transcribe a video
whispercpp transcribe video.mp4 --model base --threads 4

# Transcribe without GPU (CPU-only)
whispercpp transcribe video.mp4 --model small --no-gpu
```

### Model Management

```python
import whispercpp

# List available models
whispercpp.list_models()

# Download a specific model
whispercpp.download_model("medium")

# Force re-download
whispercpp.download_model("base", force=True)
```

### Command Line Test

```bash
# Make sure you're in your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run from project root
python test_transcribe.py video.mp4
```

---

## 📊 Benchmarking & Performance

### Run Performance Tests

The included benchmark script helps you find the optimal configuration for your hardware:

```bash
# Test with 5 video copies
PYTHONPATH=build python benchmark.py video.mp4 5
```

### What the Benchmark Tests

1. **Thread Scaling**: Tests different thread counts (1, 2, 4, 8, 16, etc.) for single video transcription
2. **Sequential Processing**: Measures throughput when processing multiple videos one after another
3. **Parallel Processing**: Tests concurrent processing with different numbers of workers
4. **Optimal Configuration**: Provides the best settings for your specific hardware

### Benchmark Output Example

```
============================================================
📊 Single Video - Thread Scaling
============================================================
System: 10 cores, 16.0GB RAM
Threads  Mean (s)   Std (s)    Min (s)    Max (s)   
--------------------------------------------------
1        1.49       0.04       1.45       1.53      
2        1.43       0.02       1.41       1.45      
4        1.43       0.03       1.40       1.45      
8        1.42       0.02       1.40       1.43      
16       1.40       0.01       1.38       1.41      

🏆 Optimal thread count: 16 (avg: 1.40s)

============================================================
🏆 BEST CONFIGURATION FOR REPRODUCTION
============================================================
Single video transcription:
  threads = 16
  model = models/ggml-base.en.bin

Batch processing (5 videos):
  Use parallel processing with 2 workers
  Each worker uses 16 threads
  Expected throughput: 1.43 videos/second

Python code example:
  import whispercpp
  from concurrent.futures import ThreadPoolExecutor
  
  def transcribe_video(video_path):
      return whispercpp.transcribe_video(video_path, 'models/ggml-base.en.bin', 16)
  
  with ThreadPoolExecutor(max_workers=2) as executor:
      results = list(executor.map(transcribe_video, video_paths))
```

### Performance Optimization Tips

1. **GPU Acceleration**: The system automatically uses Metal (macOS) or CUDA (Linux/Windows) when available
2. **Thread Count**: Use the benchmark to find optimal thread count for your CPU
3. **Batch Processing**: For multiple videos, use parallel processing with ThreadPoolExecutor
4. **Model Size**: Smaller models (base, small) are faster but less accurate than larger ones (medium, large)

---

## ⚙️ API Reference

### `transcribe_video(video_path, model, threads)`

Transcribes a video file using Whisper.

**Parameters:**
- `video_path` (str): Path to the video file
- `model` (str): Model name (e.g. "base", "tiny", etc.) or path to Whisper model binary (.bin file)
- `threads` (int): Number of CPU threads to use (default: 4)

**Returns:**
- `str`: Transcribed text

**Example:**
```python
import whispercpp

# Basic usage
text = whispercpp.transcribe_video("sample.mp4")
```

---

## License

MIT