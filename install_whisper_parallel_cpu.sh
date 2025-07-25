#!/bin/bash
# Install script for whisper_parallel_cpu with fallback options
# This script ensures the package installs correctly on different platforms

set -e  # Exit on any error

echo "Installing whisper_parallel_cpu..."

# Function to test if the package can be imported
test_import() {
    python -c "import whisper_parallel_cpu; print('✓ whisper_parallel_cpu imported successfully')" 2>/dev/null
}

# Function to install system dependencies
install_system_deps() {
    echo "Installing system dependencies..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y ffmpeg cmake build-essential
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y ffmpeg cmake gcc-c++
    elif command -v brew &> /dev/null; then
        # macOS
        brew install ffmpeg cmake
    else
        echo "Warning: Could not install system dependencies automatically"
        echo "Please ensure ffmpeg and cmake are installed manually"
    fi
}

# Try different installation methods
echo "Attempting to install whisper_parallel_cpu..."

# Method 1: Try installing from PyPI first
echo "Method 1: Installing from PyPI..."
if pip install whisper-parallel-cpu; then
    if test_import; then
        echo "✓ Successfully installed from PyPI"
        exit 0
    else
        echo "✗ Package installed but import failed, trying next method..."
        pip uninstall -y whisper-parallel-cpu
    fi
else
    echo "✗ PyPI installation failed, trying next method..."
fi

# Method 2: Install system dependencies and try again
echo "Method 2: Installing system dependencies and trying PyPI again..."
install_system_deps
if pip install whisper-parallel-cpu; then
    if test_import; then
        echo "✓ Successfully installed from PyPI after installing system dependencies"
        exit 0
    else
        echo "✗ Package installed but import failed, trying next method..."
        pip uninstall -y whisper-parallel-cpu
    fi
else
    echo "✗ PyPI installation failed, trying next method..."
fi

# Method 3: Force build from source
echo "Method 3: Building from source..."
if pip install --no-binary=whisper-parallel-cpu whisper-parallel-cpu; then
    if test_import; then
        echo "✓ Successfully built and installed from source"
        exit 0
    else
        echo "✗ Build succeeded but import failed, trying next method..."
        pip uninstall -y whisper-parallel-cpu
    fi
else
    echo "✗ Build from source failed, trying next method..."
fi

# Method 4: Install from GitHub
echo "Method 4: Installing from GitHub..."
if pip install git+https://github.com/krisfur/whisper-parallel-cpu.git; then
    if test_import; then
        echo "✓ Successfully installed from GitHub"
        exit 0
    else
        echo "✗ GitHub installation succeeded but import failed"
        pip uninstall -y whisper-parallel-cpu
    fi
else
    echo "✗ GitHub installation failed"
fi

# If we get here, all methods failed
echo "✗ All installation methods failed!"
echo "Please check the error messages above and ensure:"
echo "1. You have Python 3.8+ installed"
echo "2. You have a C++ compiler (gcc/g++ or clang) installed"
echo "3. You have cmake >= 3.15 installed"
echo "4. You have ffmpeg installed"
echo "5. You have sufficient disk space and permissions"

exit 1 