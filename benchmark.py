#!/usr/bin/env python3
"""
Benchmark script for whisper_parallel_cpu transcriber
Tests scaling with multiple videos and different thread configurations
"""

import sys
import os
import time
import statistics
import multiprocessing
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import psutil
import gc
import whisper_parallel_cpu
from typing import Dict, List, Any, Union

def get_system_info() -> Dict[str, Any]:
    """Get system information for benchmarking context"""
    cpu_freq = psutil.cpu_freq()
    freq_value = cpu_freq.current if cpu_freq else 0
    
    info = {
        'cpu_count': multiprocessing.cpu_count(),
        'cpu_freq': freq_value,
        'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'platform': sys.platform
    }
    return info

def single_transcription(video_path: str, model_path: str, threads: int, use_gpu: bool = True) -> Dict[str, Any]:
    """Single transcription with timing"""
    start_time = time.time()
    try:
        result = whisper_parallel_cpu.transcribe_video(video_path, model_path, threads, use_gpu)
        end_time = time.time()
        return {
            'success': True,
            'duration': end_time - start_time,
            'text_length': len(result),
            'result': result[:100] + "..." if len(result) > 100 else result
        }
    except Exception as e:
        end_time = time.time()
        return {
            'success': False,
            'duration': end_time - start_time,
            'error': str(e)
        }

def benchmark_single_video_threads(video_path, model_path, thread_counts):
    """Benchmark single video with different thread counts"""
    print(f"\n🔧 Benchmarking single video with different thread counts...")
    print(f"Video: {video_path}")
    print(f"Model: {model_path}")
    
    results = {}
    
    for threads in thread_counts:
        print(f"\n  Testing with {threads} threads...")
        
        # Run multiple times for statistical significance
        times = []
        for i in range(3):  # 3 runs per configuration
            print(f"    Run {i+1}/3...", end=" ", flush=True)
            result = single_transcription(video_path, model_path, threads)
            if result['success']:
                times.append(result['duration'])
                print(f"✓ {result['duration']:.2f}s")
            else:
                print(f"✗ Error: {result['error']}")
                break
        
        if times:
            results[threads] = {
                'mean': statistics.mean(times),
                'std': statistics.stdev(times) if len(times) > 1 else 0,
                'min': min(times),
                'max': max(times),
                'samples': len(times)
            }
    
    return results

def benchmark_multiple_videos_sequential(video_paths, model_path, threads):
    """Benchmark multiple videos processed sequentially"""
    print(f"\n📹 Benchmarking {len(video_paths)} videos sequentially...")
    print(f"Threads per transcription: {threads}")
    
    start_time = time.time()
    results = []
    
    for i, video_path in enumerate(video_paths, 1):
        print(f"  Processing video {i}/{len(video_paths)}: {os.path.basename(video_path)}")
        result = single_transcription(video_path, model_path, threads)
        results.append(result)
        if not result['success']:
            print(f"    ✗ Failed: {result['error']}")
            break
    
    total_time = time.time() - start_time
    
    successful_results = [r for r in results if r['success']]
    if successful_results:
        avg_time = statistics.mean([r['duration'] for r in successful_results])
        return {
            'total_time': total_time,
            'avg_per_video': avg_time,
            'successful': len(successful_results),
            'total': len(video_paths),
            'throughput': len(successful_results) / total_time
        }
    else:
        return {'error': 'All transcriptions failed'}

def benchmark_multiple_videos_parallel(video_paths, model_path, threads_per_job, max_workers):
    """Benchmark multiple videos processed in parallel"""
    print(f"\n🚀 Benchmarking {len(video_paths)} videos in parallel...")
    print(f"Threads per transcription: {threads_per_job}")
    print(f"Max parallel workers: {max_workers}")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(single_transcription, video_path, model_path, threads_per_job)
            for video_path in video_paths
        ]
        
        results = []
        for i, future in enumerate(futures, 1):
            print(f"  Waiting for video {i}/{len(video_paths)}...")
            result = future.result()
            results.append(result)
            if not result['success']:
                print(f"    ✗ Failed: {result['error']}")
    
    total_time = time.time() - start_time
    
    successful_results = [r for r in results if r['success']]
    if successful_results:
        avg_time = statistics.mean([r['duration'] for r in successful_results])
        return {
            'total_time': total_time,
            'avg_per_video': avg_time,
            'successful': len(successful_results),
            'total': len(video_paths),
            'throughput': len(successful_results) / total_time,
            'speedup': (len(successful_results) * avg_time) / total_time if total_time > 0 else 0
        }
    else:
        return {'error': 'All transcriptions failed'}

def print_benchmark_results(title, results, system_info):
    """Print formatted benchmark results"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    
    if 'error' in results:
        print(f"❌ {results['error']}")
        return
    
    # Check if this is single video results (has 'mean' key in first item)
    if results and isinstance(results, dict) and any(isinstance(data, dict) and 'mean' in data for data in results.values()):
        print(f"System: {system_info['cpu_count']} cores, {system_info['memory_gb']}GB RAM")
        print(f"{'Threads':<8} {'Mean (s)':<10} {'Std (s)':<10} {'Min (s)':<10} {'Max (s)':<10}")
        print("-" * 50)
        
        for threads, data in sorted(results.items()):
            print(f"{threads:<8} {data['mean']:<10.2f} {data['std']:<10.2f} "
                  f"{data['min']:<10.2f} {data['max']:<10.2f}")
        
        # Find optimal thread count
        if results:
            optimal = min(results.items(), key=lambda x: x[1]['mean'])
            print(f"\n🏆 Optimal thread count: {optimal[0]} (avg: {optimal[1]['mean']:.2f}s)")
    
    else:  # Multiple videos
        print(f"Total videos: {results['total']}")
        print(f"Successful: {results['successful']}")
        print(f"Total time: {results['total_time']:.2f}s")
        print(f"Average per video: {results['avg_per_video']:.2f}s")
        print(f"Throughput: {results['throughput']:.2f} videos/second")
        if 'speedup' in results:
            print(f"Speedup vs sequential: {results['speedup']:.2f}x")

def main():
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <video_file> [num_copies]")
        print("Example: python benchmark.py video.mp4 10")
        sys.exit(1)
    
    video_path = sys.argv[1]
    num_copies = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found")
        sys.exit(1)
    
    # Check for model
    model_path = "models/ggml-base.en.bin"
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found")
        print("Please download a model first:")
        print("mkdir -p models && curl -L -o models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin")
        sys.exit(1)
    
    # Get system info
    system_info = get_system_info()
    print(f"🖥️  System: {system_info['cpu_count']} cores, {system_info['memory_gb']}GB RAM")
    
    # Create list of video paths (same video repeated)
    video_paths = [video_path] * num_copies
    
    # Test 1: Single video with different thread counts
    thread_counts = [1, 2, 4, 8, 16]
    cpu_count = system_info['cpu_count']
    if cpu_count > 16:
        thread_counts.append(cpu_count)
    
    single_results = benchmark_single_video_threads(video_path, model_path, thread_counts)
    print_benchmark_results("Single Video - Thread Scaling", single_results, system_info)
    
    # Test 2: Multiple videos sequential
    print(f"\n{'='*60}")
    print(f"📹 Creating {num_copies} copies for batch testing...")
    print(f"{'='*60}")
    
    # Use optimal thread count from single video test
    optimal_threads = min(single_results.items(), key=lambda x: x[1]['mean'])[0] if single_results else 4
    
    sequential_results = benchmark_multiple_videos_sequential(video_paths, model_path, optimal_threads)
    print_benchmark_results("Multiple Videos - Sequential", sequential_results, system_info)
    
    # Test 3: Multiple videos parallel
    max_workers_options = [1, 2, 4, 8]
    cpu_count = system_info['cpu_count']
    if cpu_count > 8:
        max_workers_options.append(cpu_count)
    
    print(f"\n{'='*60}")
    print(f"🚀 Testing parallel processing with different worker counts...")
    print(f"{'='*60}")
    
    for max_workers in max_workers_options:
        if max_workers > len(video_paths):  # type: ignore
            continue
            
        parallel_results = benchmark_multiple_videos_parallel(
            video_paths, model_path, optimal_threads, max_workers
        )
        print_benchmark_results(f"Multiple Videos - Parallel ({max_workers} workers)", 
                               parallel_results, system_info)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📋 SUMMARY")
    print(f"{'='*60}")
    print(f"Optimal thread count per transcription: {optimal_threads}")
    print(f"System CPU cores: {system_info['cpu_count']}")
    print(f"Tested with {num_copies} video copies")
    
    if sequential_results and 'throughput' in sequential_results:
        print(f"Sequential throughput: {sequential_results['throughput']:.2f} videos/second")
    
    # Find best parallel result
    best_parallel = None
    best_throughput = 0
    best_workers = 0
    for max_workers in max_workers_options:
        if max_workers > len(video_paths):  # type: ignore
            continue
        parallel_results = benchmark_multiple_videos_parallel(
            video_paths, model_path, optimal_threads, max_workers
        )
        if 'throughput' in parallel_results and parallel_results['throughput'] > best_throughput:  # type: ignore
            best_throughput = parallel_results['throughput']
            best_parallel = parallel_results
            best_workers = max_workers
    
    if best_parallel:
        print(f"Best parallel throughput: {best_parallel['throughput']:.2f} videos/second")
        print(f"Speedup vs sequential: {best_parallel['speedup']:.2f}x")
    
    # Best configuration for reproduction
    print(f"\n{'='*60}")
    print(f"🏆 BEST CONFIGURATION FOR REPRODUCTION")
    print(f"{'='*60}")
    print(f"Single video transcription:")
    print(f"  threads = {optimal_threads}")
    print(f"  model = {model_path}")
    print(f"")
    print(f"Batch processing ({num_copies} videos):")
    if best_parallel and best_parallel['speedup'] > 1.1:  # type: ignore
        print(f"  Use parallel processing with {best_workers} workers")
        print(f"  Each worker uses {optimal_threads} threads")
        print(f"  Expected throughput: {best_parallel['throughput']:.2f} videos/second")
    else:
        print(f"  Use sequential processing")
        print(f"  Each transcription uses {optimal_threads} threads")
        print(f"  Expected throughput: {sequential_results['throughput']:.2f} videos/second")
    print(f"")
    print(f"Python code example:")
    print(f"  import whisper_parallel_cpu")
    if best_parallel and best_parallel['speedup'] > 1.1:  # type: ignore
        print(f"  from concurrent.futures import ThreadPoolExecutor")
        print(f"  ")
        print(f"  def transcribe_video(video_path):")
        print(f"      return whisper_parallel_cpu.transcribe_video(video_path, '{model_path}', {optimal_threads})")
        print(f"  ")
        print(f"  with ThreadPoolExecutor(max_workers={best_workers}) as executor:")
        print(f"      results = list(executor.map(transcribe_video, video_paths))")
    else:
        print(f"  ")
        print(f"  for video_path in video_paths:")
        print(f"      result = whisper_parallel_cpu.transcribe_video(video_path, '{model_path}', {optimal_threads})")

if __name__ == "__main__":
    main() 