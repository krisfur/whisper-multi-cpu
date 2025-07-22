# Release Notes - Version 1.2.0

## 🚀 New Features

### Model Reuse with WhisperModel Class

The biggest new feature in this release is the `WhisperModel` class, which allows you to load a model once and reuse it for multiple transcriptions. This provides significant performance improvements when processing multiple files.

#### Key Benefits:
- **2-5x faster** for multiple transcriptions with the same model
- **Reduced memory usage** through context sharing
- **Better for batch processing** workflows
- **Automatic model management** with context manager support

#### Usage Examples:

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

### Context Management Functions

New utility functions for managing whisper contexts:

```python
import whisper_parallel_cpu

# Clear all cached contexts to free memory
whisper_parallel_cpu.clear_contexts()

# Get the number of currently cached contexts
count = whisper_parallel_cpu.get_context_count()
print(f"Active contexts: {count}")
```

### Enhanced Performance

- **Context reuse**: Models are now cached and reused across transcription calls
- **Lazy loading**: Models are loaded only when first needed
- **Thread-safe**: Context management is thread-safe for concurrent usage
- **Memory efficient**: Automatic cleanup and manual memory management options

## 🔧 Technical Improvements

### C++ Backend Enhancements
- Added `WhisperContextManager` class for efficient context management
- Implemented thread-safe context caching with mutex protection
- Added legacy transcription functions for backward compatibility
- Enhanced memory management with automatic cleanup

### Python API Improvements
- New `WhisperModel` class with intuitive interface
- Context manager support for automatic resource management
- Enhanced error handling and validation
- Improved documentation and type hints

## 📚 Documentation Updates

- Added comprehensive documentation for the new `WhisperModel` class
- Updated README with performance comparison examples
- Added API reference for new functions
- Included usage examples and best practices

## 🔄 Backward Compatibility

This release maintains full backward compatibility with existing code:

- All existing functions (`transcribe`, `transcribe_audio`, `transcribe_video`) continue to work
- Existing function signatures remain unchanged
- Performance improvements are automatically applied to existing functions
- No breaking changes to the public API

## 🧪 Testing

- Added comprehensive test suite for new functionality
- Performance benchmarks comparing old vs new approaches
- Memory management tests
- Backward compatibility verification

## 📦 Installation

```bash
pip install whisper-parallel-cpu==1.2.0
```

## 🎯 Migration Guide

### For New Users
Start with the `WhisperModel` class for best performance:

```python
from whisper_parallel_cpu import WhisperModel

model = WhisperModel(model="base")
text = model.transcribe("audio.mp3")
```

### For Existing Users
Your existing code will continue to work and automatically benefit from performance improvements:

```python
import whisper_parallel_cpu

# This now uses context reuse internally
text = whisper_parallel_cpu.transcribe("audio.mp3", model="base")
```

### For Batch Processing
Upgrade to `WhisperModel` for significant performance gains:

```python
# Before (slower)
for file in files:
    text = whisper_parallel_cpu.transcribe(file, model="base")

# After (faster)
model = WhisperModel(model="base")
for file in files:
    text = model.transcribe(file)
```

## 🐛 Bug Fixes

- Fixed potential memory leaks in context management
- Improved error handling for model loading failures
- Enhanced thread safety for concurrent usage

## 🔮 Future Plans

- GPU memory optimization for large models
- Batch transcription API for even better performance
- Model quantization support for reduced memory usage
- Streaming transcription capabilities

---

**Note**: This release introduces significant performance improvements while maintaining full backward compatibility. Existing users will automatically benefit from the enhancements without any code changes required. 