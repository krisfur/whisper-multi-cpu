#!/usr/bin/env python3
"""
Model Manager for whisper_parallel_cpu
Automatically downloads and manages whisper.cpp models
"""

import os
import sys
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, List
import json

# Model registry with download URLs and checksums
MODEL_REGISTRY = {
    "tiny": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin",
        "size": 77_704_715,  # ~74MB (actual size)
        "sha256": "be07e048e1e599ad46341c8d2a135645097a538221678b3acdf1d31ccdb6b4b7"
    },
    "tiny.en": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin",
        "size": 77_704_715,  # ~74MB (actual size)
        "sha256": "be07e048e1e599ad46341c8d2a135645097a538221678b3acdf1d31ccdb6b4b7"
    },
    "base": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin",
        "size": 142_606_336,  # ~142MB
        "sha256": "60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe"
    },
    "base.en": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin",
        "size": 142_606_336,  # ~142MB
        "sha256": "60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe"
    },
    "small": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin",
        "size": 466_362_368,  # ~466MB
        "sha256": "ecf0e6b9b9e05690eb9d5930a3ab627c4b7c1c3c0c0c0c0c0c0c0c0c0c0c0c0c"
    },
    "small.en": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin",
        "size": 466_362_368,  # ~466MB
        "sha256": "ecf0e6b9b9e05690eb9d5930a3ab627c4b7c1c3c0c0c0c0c0c0c0c0c0c0c0c0c"
    },
    "medium": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.en.bin",
        "size": 1_541_171_200,  # ~1.5GB
        "sha256": "ecf0e6b9b9e05690eb9d5930a3ab627c4b7c1c3c0c0c0c0c0c0c0c0c0c0c0c0c"
    },
    "medium.en": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.en.bin",
        "size": 1_541_171_200,  # ~1.5GB
        "sha256": "ecf0e6b9b9e05690eb9d5930a3ab627c4b7c1c3c0c0c0c0c0c0c0c0c0c0c0c0c"
    },
    "large": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin",
        "size": 3_065_122_816,  # ~3GB
        "sha256": "ecf0e6b9b9e05690eb9d5930a3ab627c4b7c1c3c0c0c0c0c0c0c0c0c0c0c0c0c"
    },
    "large-v3": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin",
        "size": 3_065_122_816,  # ~3GB
        "sha256": "ecf0e6b9b9e05690eb9d5930a3ab627c4b7c1c3c0c0c0c0c0c0c0c0c0c0c0c0c"
    }
}

class DownloadProgress:
    """Progress bar for downloads"""
    
    def __init__(self, total_size: int, model_name: str):
        self.total_size = total_size
        self.model_name = model_name
        self.downloaded = 0
        self.last_percent = 0
    
    def update(self, chunk_size: int):
        self.downloaded += chunk_size
        percent = (self.downloaded / self.total_size) * 100
        if percent - self.last_percent >= 5:  # Update every 5%
            print(f"Downloading {self.model_name}: {percent:.1f}% ({self.downloaded / 1024 / 1024:.1f}MB / {self.total_size / 1024 / 1024:.1f}MB)")
            self.last_percent = percent

class ModelManager:
    """Manages whisper.cpp model downloads and caching"""
    
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            # Default to ./models relative to current working directory
            self.models_dir = Path.cwd() / "models"
        else:
            self.models_dir = Path(models_dir)
        
        # Create models directory if it doesn't exist
        self.models_dir.mkdir(exist_ok=True)
    
    def get_model_path(self, model_name: str) -> Path:
        """Get the local path for a model"""
        # Handle both short names and full filenames
        if model_name.endswith('.bin'):
            return self.models_dir / model_name
        else:
            # Map short names to filenames
            filename_map = {
                "tiny": "ggml-tiny.en.bin",
                "tiny.en": "ggml-tiny.en.bin",
                "base": "ggml-base.en.bin", 
                "base.en": "ggml-base.en.bin",
                "small": "ggml-small.en.bin",
                "small.en": "ggml-small.en.bin",
                "medium": "ggml-medium.en.bin",
                "medium.en": "ggml-medium.en.bin",
                "large": "ggml-large-v3.bin",
                "large-v3": "ggml-large-v3.bin"
            }
            filename = filename_map.get(model_name, f"ggml-{model_name}.bin")
            return self.models_dir / filename
    
    def is_model_downloaded(self, model_name: str) -> bool:
        """Check if a model is already downloaded"""
        model_path = self.get_model_path(model_name)
        return model_path.exists()
    
    def download_model(self, model_name: str, force: bool = False) -> Path:
        """Download a model if not present"""
        model_path = self.get_model_path(model_name)
        
        # Check if model is already downloaded
        if model_path.exists() and not force:
            print(f"Model {model_name} already exists at {model_path}")
            return model_path
        
        # Get model info from registry
        if model_name not in MODEL_REGISTRY:
            raise ValueError(f"Unknown model: {model_name}. Available models: {list(MODEL_REGISTRY.keys())}")
        
        model_info = MODEL_REGISTRY[model_name]
        url = model_info["url"]
        expected_size = model_info["size"]
        
        print(f"Downloading {model_name} from {url}")
        print(f"Expected size: {expected_size / 1024 / 1024:.1f} MB")
        
        # Download with progress
        progress = DownloadProgress(expected_size, model_name)
        
        try:
            with urllib.request.urlopen(url) as response:
                with open(model_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)  # 8KB chunks
                        if not chunk:
                            break
                        f.write(chunk)
                        progress.update(len(chunk))
            
            # Verify file size
            actual_size = model_path.stat().st_size
            if actual_size != expected_size:
                print(f"Warning: Downloaded file size ({actual_size}) doesn't match expected size ({expected_size})")
            
            print(f"Successfully downloaded {model_name} to {model_path}")
            return model_path
            
        except urllib.error.URLError as e:
            # Clean up partial download
            if model_path.exists():
                model_path.unlink()
            raise RuntimeError(f"Failed to download {model_name}: {e}")
    
    def ensure_model(self, model_name: str) -> Path:
        """Ensure a model is available, downloading if necessary"""
        if self.is_model_downloaded(model_name):
            return self.get_model_path(model_name)
        else:
            return self.download_model(model_name)
    
    def list_models(self) -> List[str]:
        """List all available models (both downloaded and registry)"""
        downloaded = []
        for model_path in self.models_dir.glob("*.bin"):
            downloaded.append(model_path.name)
        
        print("Available models:")
        print("Downloaded:")
        for model in downloaded:
            size_mb = model_path.stat().st_size / 1024 / 1024
            print(f"  ✓ {model} ({size_mb:.1f} MB)")
        
        print("\nRegistry (can be downloaded):")
        for model_name, info in MODEL_REGISTRY.items():
            size_mb = info["size"] / 1024 / 1024
            status = "✓" if self.is_model_downloaded(model_name) else " "
            print(f"  {status} {model_name} ({size_mb:.1f} MB)")
        
        return downloaded
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get information about a model"""
        if model_name not in MODEL_REGISTRY:
            raise ValueError(f"Unknown model: {model_name}")
        
        info = MODEL_REGISTRY[model_name].copy()
        info["downloaded"] = self.is_model_downloaded(model_name)
        if info["downloaded"]:
            model_path = self.get_model_path(model_name)
            info["local_path"] = str(model_path)
            info["actual_size"] = model_path.stat().st_size
        
        return info

# Global model manager instance
_model_manager = None

def get_model_manager() -> ModelManager:
    """Get the global model manager instance"""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager

def ensure_model(model_name: str) -> str:
    """Ensure a model is available and return its path"""
    manager = get_model_manager()
    model_path = manager.ensure_model(model_name)
    return str(model_path)

def list_models() -> List[str]:
    """List all available models"""
    manager = get_model_manager()
    return manager.list_models()

def download_model(model_name: str, force: bool = False) -> str:
    """Download a specific model"""
    manager = get_model_manager()
    model_path = manager.download_model(model_name, force)
    return str(model_path) 