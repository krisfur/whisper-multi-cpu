cmake_minimum_required(VERSION 3.15)
project(whisper_parallel_cpu LANGUAGES CXX)

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
pybind11_add_module(whisper_parallel_cpu MODULE
    whisper_parallel_cpu/bindings.cpp
    whisper_parallel_cpu/transcriber.cpp
    ${whisper_cpp_SOURCE_DIR}/examples/common-whisper.cpp
)

# Link against the whisper library and required libraries
target_link_libraries(whisper_parallel_cpu PRIVATE 
    whisper
    ${CMAKE_DL_LIBS}
)

# Include directories
target_include_directories(whisper_parallel_cpu PRIVATE 
    ${whisper_cpp_SOURCE_DIR}/include
    ${whisper_cpp_SOURCE_DIR}/ggml/include
    ${whisper_cpp_SOURCE_DIR}/examples
)

# Ensure the extension is placed in the Python package and set RPATH
set_target_properties(whisper_parallel_cpu PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/whisper_parallel_cpu
    INSTALL_RPATH "@loader_path/../lib"
    BUILD_WITH_INSTALL_RPATH TRUE
)

# Install the extension
install(TARGETS whisper_parallel_cpu
    LIBRARY DESTINATION whisper_parallel_cpu
)