#!/usr/bin/env python3
"""
WhisperModel class for reusing loaded models across multiple transcriptions
"""

import os
import tempfile
from typing import Optional, Union
from .model_manager import ensure_model, get_model_manager
from . import whisper_parallel_cpu as _extension


class WhisperModel:
    """
    A class that loads a whisper model once and reuses it for multiple transcriptions.
    This is more efficient than loading the model for each transcription call.
    """
    
    def __init__(self, model: str = "base", use_gpu: bool = False, threads: int = 4):
        """
        Initialize a WhisperModel with the specified model.
        
        Args:
            model: Model name (tiny, base, small, medium, large) or path to .bin file
            use_gpu: Whether to use GPU acceleration
            threads: Number of threads to use for transcription
        """
        self.model_name = model
        self.use_gpu = use_gpu
        self.threads = threads
        
        # Ensure the model is downloaded and get its path
        if model.endswith('.bin') and ('/' in model or '\\' in model):
            self.model_path = model
        else:
            self.model_path = ensure_model(model)
        
        # Verify the model file exists
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        # The model will be loaded lazily on first use
        self._loaded = False
    
    def _ensure_loaded(self):
        """Ensure the model is loaded by making a dummy transcription call"""
        if not self._loaded:
            # Create a minimal audio file to trigger model loading
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                # Create a minimal WAV file (44 bytes header + 1 sample)
                wav_data = (
                    b'RIFF' + (36).to_bytes(4, 'little') + b'WAVE' +
                    b'fmt ' + (16).to_bytes(4, 'little') + (1).to_bytes(2, 'little') +
                    (1).to_bytes(2, 'little') + (16000).to_bytes(4, 'little') +
                    (32000).to_bytes(4, 'little') + (2).to_bytes(2, 'little') +
                    (16).to_bytes(2, 'little') + b'data' + (0).to_bytes(4, 'little')
                )
                tmp_file.write(wav_data)
                tmp_path = tmp_file.name
            
            try:
                # This will load the model into the context manager
                _extension.transcribe_video(tmp_path, self.model_path, self.threads, self.use_gpu)
                self._loaded = True
            except Exception:
                # If transcription fails, that's okay - the model is still loaded
                self._loaded = True
            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    
    def transcribe(self, file_path: str) -> str:
        """
        Transcribe a video or audio file using the loaded model.
        
        Args:
            file_path: Path to the video or audio file
            
        Returns:
            Transcribed text
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Ensure model is loaded
        self._ensure_loaded()
        
        # Use the context-reusing transcription function
        return _extension.transcribe_video(file_path, self.model_path, self.threads, self.use_gpu)
    
    def transcribe_video(self, video_path: str) -> str:
        """
        Transcribe a video file using the loaded model.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Transcribed text
        """
        return self.transcribe(video_path)
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe an audio file using the loaded model.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        return self.transcribe(audio_path)
    
    def clear_contexts(self):
        """Clear all cached whisper contexts to free memory"""
        _extension.clear_whisper_contexts()
        self._loaded = False
    
    def get_context_count(self) -> int:
        """Get the number of currently cached whisper contexts"""
        return _extension.get_whisper_context_count()
    
    def __repr__(self):
        return f"WhisperModel(model='{self.model_name}', use_gpu={self.use_gpu}, threads={self.threads})"
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - optionally clear contexts"""
        # Don't automatically clear contexts on exit to allow reuse
        pass 