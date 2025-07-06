#!/usr/bin/env python3
"""
Example script demonstrating audio and video transcription with whisper_parallel_cpu
"""

import sys
import os
from pathlib import Path

def main():
    try:
        import whisper_parallel_cpu
        
        # Example files (you can replace these with your own files)
        video_file = "video.mp4"  # Replace with your video file
        audio_file = "audio.mp3"  # Replace with your audio file
        
        print("🎵 Whisper Parallel CPU - Audio & Video Transcription Example")
        print("=" * 60)
        
        # Check if example files exist
        if not os.path.exists(video_file):
            print(f"⚠️  Video file '{video_file}' not found. Skipping video transcription.")
            video_file = None
        
        if not os.path.exists(audio_file):
            print(f"⚠️  Audio file '{audio_file}' not found. Skipping audio transcription.")
            audio_file = None
        
        if not video_file and not audio_file:
            print("\n📝 Usage:")
            print("1. Place your video file as 'video.mp4' or audio file as 'audio.mp3' in this directory")
            print("2. Or modify this script to use your own file paths")
            print("3. Run: python example_audio_video.py")
            return
        
        # Test video transcription
        if video_file:
            print(f"\n🎬 Transcribing video: {video_file}")
            print("-" * 40)
            
            # Method 1: Direct video transcription (CPU-only by default)
            print("Method 1: transcribe_video()")
            try:
                result1 = whisper_parallel_cpu.transcribe_video(video_file, model="base", threads=4)
                print(f"Result: {result1[:100]}..." if len(result1) > 100 else f"Result: {result1}")
            except Exception as e:
                print(f"Error: {e}")
            
            # Method 2: Smart transcription (CPU-only by default)
            print("\nMethod 2: transcribe() (smart detection)")
            try:
                result2 = whisper_parallel_cpu.transcribe(video_file, model="base", threads=4)
                print(f"Result: {result2[:100]}..." if len(result2) > 100 else f"Result: {result2}")
            except Exception as e:
                print(f"Error: {e}")
        
        # Test audio transcription
        if audio_file:
            print(f"\n🎵 Transcribing audio: {audio_file}")
            print("-" * 40)
            
            # Method 1: Direct audio transcription (CPU-only by default)
            print("Method 1: transcribe_audio()")
            try:
                result1 = whisper_parallel_cpu.transcribe_audio(audio_file, model="base", threads=4)
                print(f"Result: {result1[:100]}..." if len(result1) > 100 else f"Result: {result1}")
            except Exception as e:
                print(f"Error: {e}")
            
            # Method 2: Smart transcription (CPU-only by default)
            print("\nMethod 2: transcribe() (smart detection)")
            try:
                result2 = whisper_parallel_cpu.transcribe(audio_file, model="base", threads=4)
                print(f"Result: {result2[:100]}..." if len(result2) > 100 else f"Result: {result2}")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n✅ Example completed!")
        print("\n💡 Tips:")
        print("- Use 'transcribe()' for automatic file type detection")
        print("- Use 'transcribe_video()' or 'transcribe_audio()' for specific file types")
        print("- Try different models: tiny, base, small, medium, large")
        print("- Adjust thread count based on your CPU")
        
    except ImportError as e:
        print(f"❌ Error: Could not import whisper_parallel_cpu module: {e}")
        print("Make sure you've installed the package: pip install whisper-parallel-cpu")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main() 