// bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

std::string transcribe_video(const std::string& video_path,
                             const std::string& model,
                             int threads,
                             bool use_gpu);

// Forward declaration from transcriber.cpp
std::string transcribe_video(const std::string& video_path,
                             const std::string& model,
                             int threads,
                             bool use_gpu);

namespace py = pybind11;

PYBIND11_MODULE(whisper_parallel_cpu, m) {
    m.def("transcribe_video", &transcribe_video,
          py::arg("video_path"),
          py::arg("model") = "models/ggml-base.en.bin",
          py::arg("threads") = 4,
          py::arg("use_gpu") = true,
          "Transcribe a video using whisper.cpp with C++ backend.");
}