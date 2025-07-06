#!/usr/bin/env python3
"""
Test script for whisper_parallel_cpu module
"""

import sys
import os
from pathlib import Path

def test_transcribe():
    try:
        import whisper_parallel_cpu
        
        # Test with a sample audio or video file if provided
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found")
                return False
        else:
            print("Usage: python test_transcribe.py <audio_or_video_file>")
            print("Example: python test_transcribe.py sample.mp4")
            print("Example: python test_transcribe.py audio.mp3")
            return False
        
        print(f"Transcribing: {file_path}")
        
        # Use the new smart transcribe function that detects file type automatically (CPU-only by default)
        result = whisper_parallel_cpu.transcribe(file_path, model="base", threads=4)
        
        print("\nTranscription result:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"Error: Could not import whisper_parallel_cpu module: {e}")
        print("Make sure you've built the module and are running from the build directory")
        return False
    except Exception as e:
        print(f"Error during transcription: {e}")
        return False

if __name__ == "__main__":
    success = test_transcribe()
    sys.exit(0 if success else 1) 