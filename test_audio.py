#!/usr/bin/env python3
"""
Test script for audio file transcription with whisper_parallel_cpu module
"""

import sys
import os
from pathlib import Path

def test_audio_transcribe():
    try:
        import whisper_parallel_cpu
        
        # Test with a sample audio file if provided
        if len(sys.argv) > 1:
            audio_path = sys.argv[1]
            if not os.path.exists(audio_path):
                print(f"Error: Audio file '{audio_path}' not found")
                return False
        else:
            print("Usage: python test_audio.py <audio_file>")
            print("Example: python test_audio.py sample.mp3")
            print("Example: python test_audio.py audio.wav")
            print("Example: python test_audio.py music.flac")
            return False
        
        print(f"Transcribing audio file: {audio_path}")
        
        # Test the specific audio transcription function (CPU-only by default)
        print("Testing transcribe_audio function...")
        result_audio = whisper_parallel_cpu.transcribe_audio(audio_path, model="base", threads=4)
        
        print("\nAudio transcription result:")
        print("=" * 50)
        print(result_audio)
        print("=" * 50)
        
        # Test the smart transcribe function (CPU-only by default)
        print("\nTesting smart transcribe function...")
        result_smart = whisper_parallel_cpu.transcribe(audio_path, model="base", threads=4)
        
        print("\nSmart transcription result:")
        print("=" * 50)
        print(result_smart)
        print("=" * 50)
        
        # Verify both results are the same
        if result_audio == result_smart:
            print("\n✅ Both transcription methods produced identical results!")
        else:
            print("\n❌ Warning: Transcription results differ between methods")
        
        return True
        
    except ImportError as e:
        print(f"Error: Could not import whisper_parallel_cpu module: {e}")
        print("Make sure you've built the module and are running from the build directory")
        return False
    except Exception as e:
        print(f"Error during transcription: {e}")
        return False

if __name__ == "__main__":
    success = test_audio_transcribe()
    sys.exit(0 if success else 1) 