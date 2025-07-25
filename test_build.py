#!/usr/bin/env python3
"""
Test script to verify whisper_parallel_cpu can be imported and built correctly.
This helps diagnose build issues on different platforms.
"""

import sys
import os

def test_import():
    """Test if the package can be imported successfully."""
    try:
        print("Testing import of whisper_parallel_cpu...")
        import whisper_parallel_cpu
        print("✓ Successfully imported whisper_parallel_cpu")
        
        # Test basic functionality
        print("Testing basic functionality...")
        whisper_parallel_cpu.list_models()
        print("✓ Basic functionality works")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Runtime error: {e}")
        return False

def test_extension():
    """Test if the C++ extension can be imported."""
    try:
        print("Testing C++ extension import...")
        from whisper_parallel_cpu import whisper_parallel_cpu as _extension
        print("✓ C++ extension imported successfully")
        return True
    except ImportError as e:
        print(f"✗ C++ extension import failed: {e}")
        return False

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Architecture: {os.uname().machine if hasattr(os, 'uname') else 'unknown'}")
    print()
    
    success = True
    success &= test_extension()
    success &= test_import()
    
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1) 