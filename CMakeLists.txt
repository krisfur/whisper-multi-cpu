cmake_minimum_required(VERSION 3.15)
project(whispercpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

# Find Python and pybind11
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

# Fetch pybind11 directly
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# Fetch whisper.cpp
FetchContent_Declare(
    whisper_cpp
    GIT_REPOSITORY https://github.com/ggerganov/whisper.cpp.git
    GIT_TAG        master
)
FetchContent_MakeAvailable(whisper_cpp)

# Create the Python extension
pybind11_add_module(whispercpp MODULE
    whispercpp/bindings.cpp
    whispercpp/transcriber.cpp
    ${whisper_cpp_SOURCE_DIR}/examples/common-whisper.cpp
)

# Link against the whisper library and required libraries
target_link_libraries(whispercpp PRIVATE 
    whisper
    ${CMAKE_DL_LIBS}
)

# Include directories
target_include_directories(whispercpp PRIVATE 
    ${whisper_cpp_SOURCE_DIR}/include
    ${whisper_cpp_SOURCE_DIR}/ggml/include
    ${whisper_cpp_SOURCE_DIR}/examples
)

# Ensure the extension is placed in the Python package
set_target_properties(whispercpp PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/whispercpp
)