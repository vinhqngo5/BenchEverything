cmake_minimum_required(VERSION 3.15)

# Use our helper function to add this benchmark experiment
add_benchmark_experiment(
  NAME float_addition
  SRCS ${CMAKE_CURRENT_SOURCE_DIR}/src/benchmark.cpp
)