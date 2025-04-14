#include <benchmark/benchmark.h>

// Simple integer addition benchmark
static void BM_IntAddition(benchmark::State& state) {
  // Setup
  int a = 42;
  int b = 24;
  int result = 0;
  
  // Benchmark loop
  for (auto _ : state) {
    // This is the operation we're benchmarking
    result = a + b;
    
    // Prevent compiler from optimizing away the result
    benchmark::DoNotOptimize(result);
  }
}

// Register the benchmark function
BENCHMARK(BM_IntAddition);

// Run the benchmark
BENCHMARK_MAIN();