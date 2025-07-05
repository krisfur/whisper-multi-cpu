# Import the C++ extension functions
try:
    # Try to import the extension directly - this should work in installed packages
    from . import whisper_parallel_cpu as _extension  # type: ignore
    _transcribe_video_impl = _extension.transcribe_video
except ImportError:
    # Fallback for development or if extension is not available
    def _transcribe_video_impl(*args, **kwargs):
        raise ImportError("C++ extension not available. Please rebuild the package.")

# Import Python modules
from .model_manager import ensure_model, list_models, download_model, get_model_manager

# Re-export the original function
__all__ = ['transcribe_video', 'transcribe', 'list_models', 'download_model', 'ensure_model']

def transcribe_video(video_path: str, model: str = "base", threads: int = 4, use_gpu: bool = True) -> str:
    """
    Transcribe a video file using whisper.cpp with automatic model downloading.
    
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

# Alias for convenience
transcribe = transcribe_video 