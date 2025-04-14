# Helper function to add a benchmark experiment
function(add_benchmark_experiment)
  # Parse arguments
  set(options)
  set(oneValueArgs NAME)
  set(multiValueArgs SRCS)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Create the executable target
  add_executable(${ARG_NAME}_benchmark ${ARG_SRCS})
  
  # Link against Google Benchmark
  target_link_libraries(${ARG_NAME}_benchmark PRIVATE benchmark::benchmark benchmark::benchmark_main)
  
  # Add include directories
  target_include_directories(${ARG_NAME}_benchmark PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
endfunction()