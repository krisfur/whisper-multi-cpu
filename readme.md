# WhisperCPP Video Transcriber

High-performance video transcription tool using [`whisper.cpp`](https://github.com/ggerganov/whisper.cpp), exposed to Python via `pybind11`.

This project:
- Extracts audio from videos using `ffmpeg`
- Transcribes using Whisper models via direct C++ library integration
- Leverages multiple CPU threads and GPU acceleration for scalable performance
- Avoids Python GIL limitations with native C++ implementation

---

## 🚀 Features

- **Direct Library Integration**: Uses whisper.cpp library directly (no subprocess calls)
- **High Performance**: Native C++ implementation with multi-threading and GPU acceleration
- **Easy Python Interface**: Simple pybind11 bindings
- **Input**: `.mp4`, `.mkv`, or any video format `ffmpeg` supports
- **Output**: Transcribed text as a Python string
- **Benchmarking**: Built-in performance testing and optimization tools

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

## 🔧 Quick Setup

1. **Clone whisper.cpp** (if not already done):
```bash
git clone https://github.com/ggerganov/whisper.cpp
```

2. **Set up Python virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pybind11 psutil
```

3. **Build the project**:
```bash
./build.sh
```

4. **Download a model**:
```bash
mkdir -p models
curl -L -o models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

---

## 🧪 Usage

### Python API

```python
import whispercpp

# Transcribe a video file
text = whispercpp.transcribe_video(
    "video.mp4", 
    model="models/ggml-base.en.bin", 
    threads=4
)
print(text)
```

### Command Line Test

```bash
# Make sure you're in your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run from project root
PYTHONPATH=build python test_transcribe.py video.mp4
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
- `model` (str): Path to Whisper model binary (.bin file)
- `threads` (int): Number of CPU threads to use (default: 4)

**Returns:**
- `str`: Transcribed text

**Example:**
```python
import whispercpp

# Basic usage
text = whispercpp.transcribe_video("sample.mp4")

# Advanced usage with custom parameters
text = whispercpp.transcribe_video(
    "sample.mp4",
    model="models/ggml-large-v3.bin",
    threads=8
)
```

### Batch Processing Example

```python
import whispercpp
from concurrent.futures import ThreadPoolExecutor
import os

def transcribe_video(video_path, model="models/ggml-base.en.bin", threads=4):
    return whispercpp.transcribe_video(video_path, model, threads)

# List of video files
video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]

# Sequential processing
results_sequential = []
for video in video_files:
    result = transcribe_video(video)
    results_sequential.append(result)

# Parallel processing (faster for multiple videos)
with ThreadPoolExecutor(max_workers=2) as executor:
    results_parallel = list(executor.map(
        lambda v: transcribe_video(v), 
        video_files
    ))
```

---

## 🏗️ Architecture

### Key Improvements

1. **Direct Library Integration**: Uses `whisper.h` and `common-whisper.h` directly instead of CLI calls
2. **Memory Management**: Proper RAII with `std::unique_ptr` for whisper context
3. **Error Handling**: Comprehensive exception handling with cleanup
4. **Performance**: No subprocess overhead, direct memory access
5. **GPU Acceleration**: Automatic Metal/GPU backend detection and usage

### Build Process

1. **CMake Integration**: Links against whisper.cpp library directly
2. **pybind11**: Creates Python module with C++ bindings
3. **Multi-threading**: Leverages whisper.cpp's built-in threading
4. **Audio Processing**: Uses ffmpeg for optimized audio conversion

---

## 🛠️ Development

### Manual Build

```bash
mkdir build && cd build
cmake ..
make -j$(nproc)  # On macOS: make -j$(sysctl -n hw.ncpu)
```

### Project Structure

```
whisper-multi-cpu/
├── CMakeLists.txt          # Build configuration
├── bindings.cpp            # Python bindings
├── transcriber.cpp         # Core transcription logic
├── benchmark.py            # Performance testing script
├── test_transcribe.py      # Test script
├── build.sh               # Automated build script
├── whisper.cpp/           # Submodule (whisper.cpp library)
└── models/                # Model files directory
```

---

## 📦 PyPI Packaging

To make this a distributable Python package on PyPI, you would need to:

### 1. Create `setup.py`

```python
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "whispercpp",
        ["bindings.cpp", "transcriber.cpp", "whisper.cpp/examples/common-whisper.cpp"],
        include_dirs=[
            "whisper.cpp/include",
            "whisper.cpp/ggml/include", 
            "whisper.cpp/examples"
        ],
        libraries=["whisper"],
        cxx_std=17,
    ),
]

setup(
    name="whispercpp",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="High-performance video transcription using whisper.cpp",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/whisper-multi-cpu",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pybind11>=2.11.0",
        "psutil>=5.8.0",
    ],
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
```

### 2. Create `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "pybind11>=2.11.0"]
build-backend = "setuptools.build_meta"

[project]
name = "whispercpp"
version = "0.1.0"
description = "High-performance video transcription using whisper.cpp"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "psutil>=5.8.0",
]
```

### 3. Build and Distribute

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (test first)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### 4. Installation for Users

```bash
pip install whispercpp
```

**Note**: The PyPI version would need to handle the whisper.cpp dependency differently (either bundle it or provide installation instructions).

---

## 🧠 Performance Notes

- **GPU Acceleration**: Automatically uses Metal (macOS) or CUDA (Linux/Windows) when available
- **CPU Multi-threading**: Configurable thread count for your hardware
- **Memory Efficient**: Processes audio in chunks
- **Fast Audio Extraction**: Uses ffmpeg for optimized audio conversion

---

## 🚨 Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're running from the project root with `PYTHONPATH=build`
2. **Model Not Found**: Download the model file to `models/` directory
3. **ffmpeg Missing**: Install ffmpeg using the instructions above
4. **Build Errors**: Ensure you have C++17 compiler and cmake >= 3.15
5. **Python Environment**: Make sure you're in your virtual environment

### Virtual Environment Issues

If you get import errors, ensure your virtual environment is activated:
```bash
# Check if you're in a virtual environment
which python  # Should show path to your venv

# Activate if needed
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Debug Mode

To see detailed build information:
```bash
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make VERBOSE=1
```

### Benchmark Issues

If the benchmark fails:
1. Ensure `psutil` is installed: `pip install psutil`
2. Check that the model file exists in `models/`
3. Verify ffmpeg is installed and accessible

---

## 🔮 Future Enhancements

- [ ] GPU acceleration support for more backends
- [ ] Real-time streaming transcription
- [ ] Batch processing multiple files
- [ ] Audio chunking for long-form content
- [ ] Language detection and selection
- [ ] Timestamp output option
- [ ] Web interface
- [ ] Docker containerization
- [ ] PyPI distribution
- [ ] Model caching and reuse
- [ ] Progress callbacks
- [ ] Custom audio preprocessing