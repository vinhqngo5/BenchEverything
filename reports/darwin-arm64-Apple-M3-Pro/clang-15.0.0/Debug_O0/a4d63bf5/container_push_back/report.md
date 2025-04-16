# Container Push Back Performance Benchmark

This benchmark compares the performance of `push_back` operations for different C++ containers:
- `std::vector<int>`
- `std::deque<int>`
- `std::list<int>`

The benchmark measures how performance scales across different container sizes, from 1,024 to 262,144 elements.

## Environment

| Property           | Value |
|--------------------|-------|
| Experiment Name    | container_push_back |
| Timestamp          | 2025-04-16T18:01:37.937107 |
| Platform (Detailed) | darwin-arm64-Apple-M3-Pro |
| Compiler (Detailed) | clang-15.0.0 |
| Build Flags        | Debug_O0 |
| Metadata Hash      | a4d63bf5 |
| CPU Model          | Apple-M3-Pro |
| Compiler Type      | clang |
| Compiler Version   | 15.0.0 |
| CMake Build Type   | Debug |
| CXX Flags Used     | -std=c++20 -O0 |


## Benchmark Results

### Raw Performance Data

| Benchmark | Time (ns) | CPU (ns) | Iterations | Items/s | Bytes/s | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ------- | ------- | ---- | ------- | ---- |
| BM_ContainerPushBack<std::vector<int>>/1024 | 31.89 | 31.89 | 21288 | 32112144.74 | 128448578.97 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/2048 | 60.80 | 60.80 | 11375 | 33683479.97 | 134733919.88 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/4096 | 115.77 | 115.79 | 6174 | 35374506.39 | 141498025.56 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/8192 | 229.93 | 229.92 | 3059 | 35630001.09 | 142520004.38 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/16384 | 441.58 | 441.21 | 1590 | 37134027.44 | 148536109.75 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/32768 | 890.19 | 890.21 | 798 | 36809477.69 | 147237910.76 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/65536 | 1864.93 | 1819.15 | 397 | 36025593.91 | 144102375.65 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/131072 | 3509.84 | 3508.32 | 200 | 37360385.26 | 149441541.02 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/262144 | 7064.31 | 7063.58 | 99 | 37112081.61 | 148448326.45 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/1024 | 57.38 | 57.39 | 12208 | 17843189.37 | 71372757.47 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/2048 | 114.51 | 114.51 | 6208 | 17884148.16 | 71536592.64 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/4096 | 250.63 | 241.12 | 3129 | 16987673.17 | 67950692.69 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/8192 | 480.40 | 476.71 | 1495 | 17184438.50 | 68737754.01 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/16384 | 938.00 | 936.25 | 734 | 17499586.73 | 69998346.93 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/32768 | 2620.20 | 2195.81 | 336 | 14922949.93 | 59691799.73 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/65536 | 3673.86 | 3673.53 | 189 | 17840065.56 | 71360262.25 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/131072 | 7117.52 | 7117.47 | 96 | 18415535.72 | 73662142.88 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/262144 | 14244.80 | 14221.57 | 51 | 18432847.10 | 73731388.39 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/1024 | 90.12 | 90.11 | 7387 | 11363642.24 | 45454568.94 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/2048 | 183.02 | 183.02 | 3740 | 11189818.09 | 44759272.35 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/4096 | 434.06 | 389.78 | 1769 | 10508473.99 | 42033895.95 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/8192 | 807.29 | 754.08 | 913 | 10863537.93 | 43454151.70 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/16384 | 1866.27 | 1573.05 | 318 | 10415432.90 | 41661731.60 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/32768 | 3650.08 | 3326.86 | 211 | 9849520.21 | 39398080.82 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/65536 | 6315.36 | 6257.79 | 111 | 10472702.14 | 41890808.58 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/131072 | 12992.75 | 12835.71 | 55 | 10211512.20 | 40846048.81 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/262144 | 25941.27 | 25453.71 | 28 | 10298850.57 | 41195402.30 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |


### Performance Across Container Sizes

The benchmark compares the time taken to insert elements into different containers, testing various container sizes to observe how each implementation scales.

Key metrics tracked:
- Items processed per second
- Bytes processed per second
- Big O computational complexity

## Complexity Analysis

Google Benchmark computed the following complexity estimations:

```
{{GBENCH_JSON:compute_complexity}}
```

## Assembly Analysis

Assembly for the vector implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>> (matched on 'BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>')
000000010000372c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
10000372c:     	stp	x28, x27, [sp, #-32]!
100003730:     	stp	x29, x30, [sp, #16]
100003734:     	add	x29, sp, #16
100003738:     	sub	sp, sp, #752
10000373c:     	str	x0, [sp, #296]
;     const int N = state.range(0);
100003740:     	ldr	x8, [sp, #296]
100003744:     	str	x8, [sp, #312]
100003748:     	str	xzr, [sp, #304]
10000374c:     	ldr	x8, [sp, #312]
100003750:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
100003754:     	add	x0, x8, #32

```

Assembly for the deque implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>> (matched on 'BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>')
0000000100003d20 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003d20:     	stp	x28, x27, [sp, #-32]!
100003d24:     	stp	x29, x30, [sp, #16]
100003d28:     	add	x29, sp, #16
100003d2c:     	sub	sp, sp, #768
100003d30:     	str	x0, [sp, #312]
;     const int N = state.range(0);
100003d34:     	ldr	x8, [sp, #312]
100003d38:     	str	x8, [sp, #328]
100003d3c:     	str	xzr, [sp, #320]
100003d40:     	ldr	x8, [sp, #328]
100003d44:     	str	x8, [sp, #136]
;     assert(range_.size() > pos);
100003d48:     	add	x0, x8, #32

```

Assembly for the list implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>> (matched on 'BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>')
00000001000042d8 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
1000042d8:     	stp	x28, x27, [sp, #-32]!
1000042dc:     	stp	x29, x30, [sp, #16]
1000042e0:     	add	x29, sp, #16
1000042e4:     	sub	sp, sp, #752
1000042e8:     	str	x0, [sp, #296]
;     const int N = state.range(0);
1000042ec:     	ldr	x8, [sp, #296]
1000042f0:     	str	x8, [sp, #312]
1000042f4:     	str	xzr, [sp, #304]
1000042f8:     	ldr	x8, [sp, #312]
1000042fc:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
100004300:     	add	x0, x8, #32

```

## All Assembly Files

### Assembly Files

- [BM_ContainerPushBack<std::deque<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5/container_push_back/assembly/BM_ContainerPushBack<std::deque<int>>.s)
- [BM_ContainerPushBack<std::list<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5/container_push_back/assembly/BM_ContainerPushBack<std::list<int>>.s)
- [BM_ContainerPushBack<std::vector<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5/container_push_back/assembly/BM_ContainerPushBack<std::vector<int>>.s)
