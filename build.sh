#!/bin/bash

# Build script for whispercpp transcriber

set -e  # Exit on any error

echo "Building whispercpp transcriber..."

# Check if we're in the right directory
if [ ! -f "CMakeLists.txt" ]; then
    echo "Error: CMakeLists.txt not found. Please run this script from the project root."
    exit 1
fi

# Create build directory
mkdir -p build
cd build

# Configure with CMake
echo "Configuring with CMake..."
cmake ..

# Build - handle different systems for parallel compilation
echo "Building..."
if command -v nproc >/dev/null 2>&1; then
    # Linux
    make -j$(nproc)
elif command -v sysctl >/dev/null 2>&1; then
    # macOS
    make -j$(sysctl -n hw.ncpu)
else
    # Fallback
    make -j4
fi

echo "Build completed successfully!"
echo ""
echo "To test the module:"
echo "1. Install the package:"
echo "   pip install -e .."
echo ""
echo "2. Run the test script:"
echo "   python ../test_transcribe.py <path_to_video_file>"
echo ""
echo "Note: Make sure you have ffmpeg installed for audio extraction."
echo "Models will be downloaded automatically on first use." 