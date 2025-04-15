#include <benchmark/benchmark.h>
#include <vector>
#include <deque>
#include <list>

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
    
    state.SetItemsProcessed(int64_t(state.iterations()) * N);
    state.SetBytesProcessed(int64_t(state.iterations()) * N * sizeof(int));
    state.SetLabel(std::to_string(N) + " elements");
}

BENCHMARK_TEMPLATE(BM_ContainerPushBack, std::vector<int>)
    ->Range(1<<10, 1<<18)
    ->Unit(benchmark::kMicrosecond)
    ->Complexity();

BENCHMARK_TEMPLATE(BM_ContainerPushBack, std::deque<int>)
    ->Range(1<<10, 1<<18)
    ->Unit(benchmark::kMicrosecond)
    ->Complexity();

BENCHMARK_TEMPLATE(BM_ContainerPushBack, std::list<int>)
    ->Range(1<<10, 1<<18)
    ->Unit(benchmark::kMicrosecond)
    ->Complexity();

BENCHMARK_MAIN();