#include <benchmark/benchmark.h>

// Simple float addition benchmark
static void BM_FloatAddition(benchmark::State& state) {
  // Setup
  float a = 42.0f;
  float b = 24.0f;
  float result = 0.0f;
  
  // Benchmark loop
  for (auto _ : state) {
    // This is the operation we're benchmarking
    result = a + b;
    
    // Prevent compiler from optimizing away the result
    benchmark::DoNotOptimize(result);
  }
}

// Register the benchmark function
BENCHMARK(BM_FloatAddition);

// Run the benchmark
BENCHMARK_MAIN();