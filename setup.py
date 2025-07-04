from skbuild import setup

setup(
    name="whispercpp",
    version="0.1.0",
    description="High-performance video transcription using whisper.cpp",
    author="Krzysztof Furman",
    packages=["whispercpp"],
    install_requires=["psutil>=5.8.0"],
) 