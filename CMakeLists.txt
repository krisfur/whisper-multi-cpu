cmake_minimum_required(VERSION 3.15)
project(whispercpp_transcriber)

set(CMAKE_CXX_STANDARD 17)

# Fetch pybind11 directly
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.11.1  # or latest
)
FetchContent_MakeAvailable(pybind11)

# Add whisper.cpp as a subdirectory
add_subdirectory(whisper.cpp)

# Python extension
pybind11_add_module(whispercpp bindings.cpp transcriber.cpp whisper.cpp/examples/common-whisper.cpp)

# Link against whisper library and required libraries
target_link_libraries(whispercpp PRIVATE 
    whisper
    ${CMAKE_DL_LIBS}
)

# Include directories for whisper.cpp
target_include_directories(whispercpp PRIVATE 
    whisper.cpp/include
    whisper.cpp/ggml/include
    whisper.cpp/examples
)