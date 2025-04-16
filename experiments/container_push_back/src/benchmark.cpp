#include <benchmark/benchmark.h>

#include <deque>
#include <list>
#include <vector>

template <typename Container>
static void BM_ContainerPushBack(benchmark::State& state) {
    const int N = state.range(0);

    for (auto _ : state) {
        state.PauseTiming();
        Container c;
        state.ResumeTiming();

        for (int i = 0; i < N; ++i) {
            c.push_back(i);
        }
    }

    // Set the complexity N value explicitly for complexity calculation
    state.SetComplexityN(N);
    state.SetItemsProcessed(int64_t(state.iterations()) * N);
    state.SetBytesProcessed(int64_t(state.iterations()) * N * sizeof(int));
    state.SetLabel(std::to_string(N) + " elements");
}

// Updated benchmarks with proper complexity calculation parameters
BENCHMARK_TEMPLATE(BM_ContainerPushBack, std::vector<int>)->RangeMultiplier(2)->Range(1 << 10, 1 << 18)->Unit(benchmark::kMicrosecond)->Complexity(benchmark::oN);

BENCHMARK_TEMPLATE(BM_ContainerPushBack, std::deque<int>)->RangeMultiplier(2)->Range(1 << 10, 1 << 18)->Unit(benchmark::kMicrosecond)->Complexity(benchmark::oN);

BENCHMARK_TEMPLATE(BM_ContainerPushBack, std::list<int>)->RangeMultiplier(2)->Range(1 << 10, 1 << 18)->Unit(benchmark::kMicrosecond)->Complexity(benchmark::oN);

BENCHMARK_MAIN();