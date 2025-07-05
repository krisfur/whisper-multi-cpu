#!/usr/bin/env python3
"""
Thread Benchmark for Cloud Containers
Tests different thread counts to find optimal performance
"""

import whisper_parallel_cpu
import time
import psutil
import sys
import os

def get_system_info():
    """Get system information"""
    print("=== System Information ===")
    print(f"CPU cores: {psutil.cpu_count()}")
    print(f"CPU cores (logical): {psutil.cpu_count(logical=True)}")
    print(f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print(f"Platform: {sys.platform}")
    print()

def benchmark_threads(video_path, model_path, max_threads=None):
    """Benchmark different thread counts"""
    if max_threads is None:
        cpu_count = psutil.cpu_count()
        max_threads = cpu_count if cpu_count is not None else 4
    
    # Ensure max_threads is a valid integer
    max_threads = int(max_threads)
    
    print(f"=== Thread Benchmark (max {max_threads} threads) ===")
    print(f"Video: {video_path}")
    print(f"Model: {model_path}")
    print()
    
    # Test CPU-only mode first (more predictable)
    print("CPU-Only Mode:")
    print("-" * 40)
    
    results_cpu = {}
    thread_counts = [1, 2, 3, 4, 6, 8][:max_threads]
    
    for threads in thread_counts:
        print(f"Testing {threads} thread(s)...", end=" ", flush=True)
        start_time = time.time()
        try:
            result = whisper_parallel_cpu.transcribe_video(video_path, model_path, threads, use_gpu=False)
            elapsed = time.time() - start_time
            results_cpu[threads] = elapsed
            print(f"✓ {elapsed:.2f}s")
        except Exception as e:
            print(f"✗ Error: {e}")
            results_cpu[threads] = None
    
    print()
    print("Results Summary (CPU-Only):")
    print("-" * 40)
    print("Threads | Time (s) | Speedup | Efficiency")
    print("-" * 40)
    
    baseline = results_cpu.get(1)
    if baseline:
        for threads in thread_counts:
            time_taken = results_cpu.get(threads)
            if time_taken:
                speedup = baseline / time_taken
                efficiency = speedup / threads * 100
                print(f"{threads:7d} | {time_taken:8.2f} | {speedup:7.2f}x | {efficiency:9.1f}%")
    
    # Test GPU mode if available
    print()
    print("GPU Mode (if available):")
    print("-" * 40)
    
    results_gpu = {}
    for threads in [1, 2, 4, 8]:
        if threads > max_threads:
            break
        print(f"Testing {threads} thread(s)...", end=" ", flush=True)
        start_time = time.time()
        try:
            result = whisper_parallel_cpu.transcribe_video(video_path, model_path, threads, use_gpu=True)
            elapsed = time.time() - start_time
            results_gpu[threads] = elapsed
            print(f"✓ {elapsed:.2f}s")
        except Exception as e:
            print(f"✗ Error: {e}")
            results_gpu[threads] = None
    
    print()
    print("Results Summary (GPU):")
    print("-" * 40)
    print("Threads | Time (s) | Speedup")
    print("-" * 40)
    
    baseline = results_gpu.get(1)
    if baseline:
        for threads in [1, 2, 4, 8]:
            if threads > max_threads:
                break
            time_taken = results_gpu.get(threads)
            if time_taken:
                speedup = baseline / time_taken
                print(f"{threads:7d} | {time_taken:8.2f} | {speedup:7.2f}x")
    
    return results_cpu, results_gpu

def get_recommendations(results_cpu, results_gpu, max_threads):
    """Provide recommendations based on results"""
    print()
    print("=== Recommendations ===")
    
    # CPU recommendations
    if results_cpu:
        best_cpu_threads = min(results_cpu.items(), key=lambda x: x[1] if x[1] else float('inf'))
        print(f"CPU-Only Mode: Use {best_cpu_threads[0]} threads (best performance)")
        
        # Conservative recommendation
        conservative = min(3, max_threads)
        print(f"CPU-Only Mode (conservative): Use {conservative} threads (leaves resources for system)")
    
    # GPU recommendations
    if results_gpu:
        best_gpu_threads = min(results_gpu.items(), key=lambda x: x[1] if x[1] else float('inf'))
        print(f"GPU Mode: Use {best_gpu_threads[0]} threads (best performance)")
    
    # General recommendations
    print()
    print("General Guidelines:")
    print(f"- For 4-core container: Start with 4 threads")
    print(f"- For shared environments: Use 3 threads (leaves 1 core free)")
    print(f"- For batch processing: Use 4 threads (maximize throughput)")
    print(f"- Monitor CPU usage and adjust based on other workloads")

if __name__ == "__main__":
    # Default values
    video_path = "video.mp4"
    model_path = "models/ggml-base.en.bin"
    max_threads = 8
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    if len(sys.argv) > 2:
        model_path = sys.argv[2]
    if len(sys.argv) > 3:
        max_threads = int(sys.argv[3])
    
    # Check if files exist
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found")
        sys.exit(1)
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found")
        sys.exit(1)
    
    get_system_info()
    results_cpu, results_gpu = benchmark_threads(video_path, model_path, max_threads)
    get_recommendations(results_cpu, results_gpu, max_threads) 