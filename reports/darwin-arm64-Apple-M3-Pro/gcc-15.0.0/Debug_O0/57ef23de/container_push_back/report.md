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
| Timestamp          | 2025-04-16T18:00:56.254186 |
| Platform (Detailed) | darwin-arm64-Apple-M3-Pro |
| Compiler (Detailed) | gcc-15.0.0 |
| Build Flags        | Debug_O0 |
| Metadata Hash      | 57ef23de |
| CPU Model          | Apple-M3-Pro |
| Compiler Type      | gcc |
| Compiler Version   | 15.0.0 |
| CMake Build Type   | Debug |
| CXX Flags Used     | -std=c++20 -O0 |


## Benchmark Results

### Raw Performance Data

| Benchmark | Time (ns) | CPU (ns) | Iterations | Items/s | Bytes/s | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ------- | ------- | ---- | ------- | ---- |
| BM_ContainerPushBack<std::vector<int>>/1024 | 52.56 | 41.07 | 22002 | 24931610.29 | 99726441.17 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/2048 | 66.54 | 65.40 | 10947 | 31314276.14 | 125257104.55 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/4096 | 124.89 | 124.34 | 5267 | 32942525.96 | 131770103.85 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/8192 | 251.26 | 237.94 | 3027 | 34428674.57 | 137714698.27 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/16384 | 459.87 | 449.33 | 1574 | 36463354.83 | 145853419.34 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/32768 | 899.80 | 899.83 | 774 | 36415684.81 | 145662739.24 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/65536 | 1762.04 | 1761.36 | 384 | 37207570.49 | 148830281.96 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/131072 | 3590.88 | 3591.01 | 192 | 36500033.36 | 146000133.44 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/262144 | 7225.18 | 7192.36 | 96 | 36447540.58 | 145790162.31 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/1024 | 59.88 | 59.88 | 11578 | 17101550.21 | 68406200.82 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/2048 | 118.89 | 118.90 | 6005 | 17224835.89 | 68899343.54 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/4096 | 233.95 | 233.96 | 2969 | 17507524.29 | 70030097.16 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/8192 | 465.99 | 465.96 | 1497 | 17580936.46 | 70323745.84 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/16384 | 941.63 | 941.62 | 769 | 17399891.18 | 69599564.70 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/32768 | 1861.44 | 1861.33 | 376 | 17604643.22 | 70418572.88 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/65536 | 3645.08 | 3645.03 | 188 | 17979540.79 | 71918163.17 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/131072 | 7211.67 | 7211.64 | 100 | 18175061.43 | 72700245.71 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/262144 | 14559.09 | 14549.44 | 48 | 18017466.31 | 72069865.24 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/1024 | 87.60 | 87.60 | 7927 | 11688878.26 | 46755513.06 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/2048 | 174.95 | 174.95 | 4020 | 11706351.58 | 46825406.30 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/4096 | 355.26 | 355.20 | 2010 | 11531596.14 | 46126384.55 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/8192 | 1133.17 | 890.61 | 961 | 9198203.01 | 36792812.03 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/16384 | 1702.19 | 1604.09 | 459 | 10213908.91 | 40855635.66 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/32768 | 3325.03 | 3235.55 | 218 | 10127502.84 | 40510011.36 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/65536 | 8305.41 | 7217.47 | 109 | 9080192.80 | 36320771.22 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/131072 | 20020.49 | 13580.07 | 54 | 9651788.30 | 38607153.18 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/262144 | 30469.34 | 27153.05 | 20 | 9654311.39 | 38617245.58 | us | 1 | 1 |
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
0000000100003748 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003748:     	stp	x28, x27, [sp, #-32]!
10000374c:     	stp	x29, x30, [sp, #16]
100003750:     	add	x29, sp, #16
100003754:     	sub	sp, sp, #752
100003758:     	str	x0, [sp, #296]
;     const int N = state.range(0);
10000375c:     	ldr	x8, [sp, #296]
100003760:     	str	x8, [sp, #312]
100003764:     	str	xzr, [sp, #304]
100003768:     	ldr	x8, [sp, #312]
10000376c:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
100003770:     	add	x0, x8, #32

```

Assembly for the deque implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>> (matched on 'BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>')
0000000100003d3c <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003d3c:     	stp	x28, x27, [sp, #-32]!
100003d40:     	stp	x29, x30, [sp, #16]
100003d44:     	add	x29, sp, #16
100003d48:     	sub	sp, sp, #768
100003d4c:     	str	x0, [sp, #312]
;     const int N = state.range(0);
100003d50:     	ldr	x8, [sp, #312]
100003d54:     	str	x8, [sp, #328]
100003d58:     	str	xzr, [sp, #320]
100003d5c:     	ldr	x8, [sp, #328]
100003d60:     	str	x8, [sp, #136]
;     assert(range_.size() > pos);
100003d64:     	add	x0, x8, #32

```

Assembly for the list implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>> (matched on 'BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>')
00000001000042f4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
1000042f4:     	stp	x28, x27, [sp, #-32]!
1000042f8:     	stp	x29, x30, [sp, #16]
1000042fc:     	add	x29, sp, #16
100004300:     	sub	sp, sp, #752
100004304:     	str	x0, [sp, #296]
;     const int N = state.range(0);
100004308:     	ldr	x8, [sp, #296]
10000430c:     	str	x8, [sp, #312]
100004310:     	str	xzr, [sp, #304]
100004314:     	ldr	x8, [sp, #312]
100004318:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
10000431c:     	add	x0, x8, #32

```

## All Assembly Files

### Assembly Files

- [BM_ContainerPushBack<std::deque<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/57ef23de/container_push_back/assembly/BM_ContainerPushBack<std::deque<int>>.s)
- [BM_ContainerPushBack<std::list<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/57ef23de/container_push_back/assembly/BM_ContainerPushBack<std::list<int>>.s)
- [BM_ContainerPushBack<std::vector<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/57ef23de/container_push_back/assembly/BM_ContainerPushBack<std::vector<int>>.s)
