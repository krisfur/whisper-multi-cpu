#!/usr/bin/env python3
"""
Test script for whispercpp module
"""

import sys
import os
from pathlib import Path

def test_transcribe():
    try:
        import whispercpp
        
        # Test with a sample video file if provided
        if len(sys.argv) > 1:
            video_path = sys.argv[1]
            if not os.path.exists(video_path):
                print(f"Error: Video file '{video_path}' not found")
                return False
        else:
            print("Usage: python test_transcribe.py <video_file>")
            print("Example: python test_transcribe.py sample.mp4")
            return False
        
        print(f"Transcribing: {video_path}")
        
        # Default model path
        model_path = "models/ggml-base.en.bin"
        
        # Check if model exists
        if not os.path.exists(model_path):
            print(f"Warning: Model file '{model_path}' not found")
            print("Please download a model file first:")
            print("mkdir -p models")
            print("curl -L -o models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin")
            return False
        
        # Transcribe with 4 threads
        result = whispercpp.transcribe_video(video_path, model_path, 4)
        
        print("\nTranscription result:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"Error: Could not import whispercpp module: {e}")
        print("Make sure you've built the module and are running from the build directory")
        return False
    except Exception as e:
        print(f"Error during transcription: {e}")
        return False

if __name__ == "__main__":
    success = test_transcribe()
    sys.exit(0 if success else 1) 