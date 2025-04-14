cmake_minimum_required(VERSION 3.15)
project(BenchEverything VERSION 1.0.0 LANGUAGES CXX)

# Set C++20 as the default standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Include FetchContent for dependencies
include(FetchContent)

# Fetch Google Benchmark
FetchContent_Declare(
  benchmark
  GIT_REPOSITORY https://github.com/google/benchmark.git
  GIT_TAG v1.8.0
)
# Configure Google Benchmark
set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "Disable benchmark testing" FORCE)
FetchContent_MakeAvailable(benchmark)

# Include our benchmark utilities
include(${CMAKE_SOURCE_DIR}/cmake/BenchmarkUtils.cmake)

# Include all experiments
add_subdirectory(experiments/int_addition)
add_subdirectory(experiments/float_addition)