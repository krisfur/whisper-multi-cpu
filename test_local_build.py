#!/usr/bin/env python3
"""
Local build test script to debug build issues before pushing to GitHub Actions.
This helps avoid wasting GitHub Actions minutes on failed builds.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"❌ {description} FAILED")
            return False
        else:
            print(f"✅ {description} SUCCESS")
            return True
    except subprocess.TimeoutExpired:
        print(f"❌ {description} TIMEOUT (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ {description} ERROR: {e}")
        return False

def check_system_info():
    """Print system information for debugging"""
    print("System Information:")
    print(f"  Platform: {platform.platform()}")
    print(f"  Architecture: {platform.architecture()}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")
    print(f"  Python: {sys.version}")

def check_dependencies():
    """Check if required dependencies are available"""
    print("\nChecking dependencies...")
    
    deps = [
        ("cmake", "cmake --version"),
        ("ffmpeg", "ffmpeg -version"),
        ("gcc", "gcc --version"),
        ("g++", "g++ --version"),
    ]
    
    for name, cmd in deps:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"  ✅ {name}: {version}")
            else:
                print(f"  ❌ {name}: Not found or not working")
        except Exception as e:
            print(f"  ❌ {name}: Error checking - {e}")

def test_build():
    """Test the build process"""
    print("\nTesting build process...")
    
    # Clean previous builds
    if Path("build").exists():
        print("Cleaning previous build...")
        run_command(["rm", "-rf", "build"], "Clean build directory")
    
    # Test pip build
    success = run_command([
        sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "--wheel-dir=./test_wheels"
    ], "Build wheel with pip")
    
    if success:
        # List created wheels
        wheel_dir = Path("./test_wheels")
        if wheel_dir.exists():
            wheels = list(wheel_dir.glob("*.whl"))
            print(f"\nCreated wheels: {len(wheels)}")
            for wheel in wheels:
                print(f"  {wheel.name}")
    
    return success

def test_install():
    """Test installing the built wheel"""
    print("\nTesting wheel installation...")
    
    wheel_dir = Path("./test_wheels")
    if not wheel_dir.exists():
        print("❌ No test wheels found")
        return False
    
    wheels = list(wheel_dir.glob("*.whl"))
    if not wheels:
        print("❌ No wheels found in test_wheels directory")
        return False
    
    # Test the first wheel
    wheel_path = wheels[0]
    success = run_command([
        sys.executable, "-m", "pip", "install", str(wheel_path)
    ], f"Install wheel: {wheel_path.name}")
    
    if success:
        # Test import
        import_success = run_command([
            sys.executable, "-c", "import whisper_parallel_cpu; print('Import successful')"
        ], "Test module import")
        
        if import_success:
            # Run the actual test
            test_success = run_command([
                sys.executable, "test_build.py"
            ], "Run test_build.py")
            
            # Cleanup
            run_command([
                sys.executable, "-m", "pip", "uninstall", "-y", "whisper-parallel-cpu"
            ], "Uninstall test package")
            
            return test_success
    
    return False

def test_cibuildwheel_config():
    """Test the cibuildwheel configuration"""
    print("\nTesting cibuildwheel configuration...")
    
    # Check if cibuildwheel is available
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "show", "cibuildwheel"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print("❌ cibuildwheel not installed. Installing...")
            run_command([
                sys.executable, "-m", "pip", "install", "cibuildwheel"
            ], "Install cibuildwheel")
        else:
            print("✅ cibuildwheel is available")
    except Exception as e:
        print(f"❌ Error checking cibuildwheel: {e}")
    
    # Test cibuildwheel configuration
    success = run_command([
        sys.executable, "-m", "cibuildwheel", "--print-build-identifiers", "."
    ], "Print build identifiers from cibuildwheel config")
    
    return success

def main():
    """Main test function"""
    print("🔧 Local Build Test for whisper-parallel-cpu")
    print("This script helps debug build issues locally before pushing to GitHub Actions")
    print("Focuses on x86_64 Linux and Apple Silicon Mac builds only")
    
    check_system_info()
    check_dependencies()
    
    # Test cibuildwheel configuration first
    config_success = test_cibuildwheel_config()
    
    build_success = test_build()
    
    if build_success:
        install_success = test_install()
        if install_success:
            print("\n🎉 All tests passed! Your build should work on GitHub Actions.")
            print("The updated config will only build for x86_64 Linux and Apple Silicon Macs.")
            return 0
        else:
            print("\n❌ Build succeeded but installation/test failed.")
            return 1
    else:
        print("\n❌ Build failed. Check the output above for issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 