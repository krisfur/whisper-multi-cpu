#!/usr/bin/env python3
"""Command-line interface for whisper_parallel_cpu model management"""

import argparse
import sys
from .model_manager import get_model_manager, list_models, download_model

def main():
    parser = argparse.ArgumentParser(description="whisper_parallel_cpu model manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List models command
    list_parser = subparsers.add_parser('list', help='List available models')
    
    # Download model command
    download_parser = subparsers.add_parser('download', help='Download a model')
    download_parser.add_argument('model', help='Model name (tiny, base, small, medium, large)')
    download_parser.add_argument('--force', action='store_true', help='Force re-download')
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser('transcribe', help='Transcribe a video file')
    transcribe_parser.add_argument('video', help='Path to video file')
    transcribe_parser.add_argument('--model', default='base', help='Model name (default: base)')
    transcribe_parser.add_argument('--threads', type=int, default=4, help='Number of threads (default: 4)')
    transcribe_parser.add_argument('--no-gpu', action='store_true', help='Disable GPU acceleration')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_models()
    
    elif args.command == 'download':
        try:
            model_path = download_model(args.model, force=args.force)
            print(f"Model downloaded to: {model_path}")
        except Exception as e:
            print(f"Error downloading model: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'transcribe':
        from . import transcribe_video
        try:
            result = transcribe_video(
                video_path=args.video,
                model=args.model,
                threads=args.threads,
                use_gpu=not args.no_gpu
            )
            print("Transcription result:")
            print(result)
        except Exception as e:
            print(f"Error transcribing video: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 