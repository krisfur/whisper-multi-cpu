# Import the C++ extension functions
try:
    # Try to import the extension directly - this should work in installed packages
    from . import whisper_parallel_cpu as _extension  # type: ignore
    _transcribe_video_impl = _extension.transcribe_video
    _transcribe_video_legacy_impl = _extension.transcribe_video_legacy
    _clear_contexts_impl = _extension.clear_whisper_contexts
    _get_context_count_impl = _extension.get_whisper_context_count
except ImportError:
    # Fallback for development or if extension is not available
    def _transcribe_video_impl(*args, **kwargs):
        raise ImportError("C++ extension not available. Please rebuild the package.")
    def _transcribe_video_legacy_impl(*args, **kwargs):
        raise ImportError("C++ extension not available. Please rebuild the package.")
    def _clear_contexts_impl(*args, **kwargs):
        raise ImportError("C++ extension not available. Please rebuild the package.")
    def _get_context_count_impl(*args, **kwargs):
        raise ImportError("C++ extension not available. Please rebuild the package.")

# Import Python modules
from .model_manager import ensure_model, list_models, download_model, get_model_manager
from .whisper_model import WhisperModel
import os
import subprocess
import tempfile

# Re-export the original function
__all__ = [
    'transcribe_video', 'transcribe_audio', 'transcribe', 
    'list_models', 'download_model', 'ensure_model',
    'WhisperModel', 'clear_contexts', 'get_context_count'
]

def transcribe_video(video_path: str, model: str = "base", threads: int = 4, use_gpu: bool = False) -> str:
    """
    Transcribe a video file using whisper.cpp with automatic model downloading.
    This function now uses context reuse for better performance on multiple calls.
    
    Args:
        video_path: Path to the video file
        model: Model name (tiny, base, small, medium, large) or path to .bin file
        threads: Number of threads to use
        use_gpu: Whether to use GPU acceleration
    
    Returns:
        Transcribed text
    """
    # If model is a path to a .bin file, use it directly
    if model.endswith('.bin') and ('/' in model or '\\' in model):
        model_path = model
    else:
        # Ensure the model is downloaded
        model_path = ensure_model(model)
    
    return _transcribe_video_impl(video_path, model_path, threads, use_gpu)

def transcribe_audio(audio_path: str, model: str = "base", threads: int = 4, use_gpu: bool = False) -> str:
    """
    Transcribe an audio file using whisper.cpp with automatic model downloading.
    This function now uses context reuse for better performance on multiple calls.
    
    Args:
        audio_path: Path to the audio file
        model: Model name (tiny, base, small, medium, large) or path to .bin file
        threads: Number of threads to use
        use_gpu: Whether to use GPU acceleration
    
    Returns:
        Transcribed text
    """
    # If model is a path to a .bin file, use it directly
    if model.endswith('.bin') and ('/' in model or '\\' in model):
        model_path = model
    else:
        # Ensure the model is downloaded
        model_path = ensure_model(model)
    
    # Create a temporary video file with the audio
    # This is a workaround since the C++ implementation expects video files
    # but we can pass audio files as "video" and ffmpeg will handle them
    return _transcribe_video_impl(audio_path, model_path, threads, use_gpu)

def _is_audio_file(file_path: str) -> bool:
    """
    Check if a file is an audio file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is an audio file, False otherwise
    """
    audio_extensions = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', 
        '.opus', '.webm', '.3gp', '.amr', '.au', '.ra', '.mid', '.midi'
    }
    return os.path.splitext(file_path.lower())[1] in audio_extensions

def _is_video_file(file_path: str) -> bool:
    """
    Check if a file is a video file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a video file, False otherwise
    """
    video_extensions = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', 
        '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts'
    }
    return os.path.splitext(file_path.lower())[1] in video_extensions

def transcribe(file_path: str, model: str = "base", threads: int = 4, use_gpu: bool = False) -> str:
    """
    Transcribe a video or audio file using whisper.cpp with automatic model downloading.
    Automatically detects file type and routes to the appropriate transcription function.
    This function now uses context reuse for better performance on multiple calls.
    
    Args:
        file_path: Path to the video or audio file
        model: Model name (tiny, base, small, medium, large) or path to .bin file
        threads: Number of threads to use
        use_gpu: Whether to use GPU acceleration
    
    Returns:
        Transcribed text
        
    Raises:
        ValueError: If the file type is not supported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if _is_audio_file(file_path):
        return transcribe_audio(file_path, model, threads, use_gpu)
    elif _is_video_file(file_path):
        return transcribe_video(file_path, model, threads, use_gpu)
    else:
        raise ValueError(f"Unsupported file type: {file_path}. Supported formats: "
                        f"Audio: mp3, wav, flac, aac, ogg, m4a, wma, opus, webm, 3gp, amr, au, ra, mid, midi. "
                        f"Video: mp4, avi, mov, mkv, wmv, flv, webm, m4v, 3gp, ogv, ts, mts, m2ts")

def clear_contexts():
    """
    Clear all cached whisper contexts to free memory.
    This is useful when you want to free up memory or switch to a different model configuration.
    """
    _clear_contexts_impl()

def get_context_count() -> int:
    """
    Get the number of currently cached whisper contexts.
    This can be useful for debugging or monitoring memory usage.
    
    Returns:
        Number of cached contexts
    """
    return _get_context_count_impl()

# The transcribe function is already defined above and handles both audio and video files 