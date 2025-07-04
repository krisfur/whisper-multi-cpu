from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "whispercpp",
        ["bindings.cpp", "transcriber.cpp", "whisper.cpp/examples/common-whisper.cpp"],
        include_dirs=[
            "whisper.cpp/include",
            "whisper.cpp/ggml/include", 
            "whisper.cpp/examples"
        ],
        libraries=["whisper"],
        cxx_std=17,
    ),
]

setup(
    name="whispercpp",
    version="0.1.0",
    author="Krzysztof Furman",
    author_email="k_furman@outlook.com",
    description="High-performance video transcription using whisper.cpp",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/krisfur/whisper-multi-cpu",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.8.0",
    ],
    extras_require={
        "dev": [
            "pybind11>=2.11.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    packages=["whispercpp"],
    package_data={
        "whispercpp": ["*.py", "*.cpp", "*.h"],
    },
    include_package_data=True,
) 