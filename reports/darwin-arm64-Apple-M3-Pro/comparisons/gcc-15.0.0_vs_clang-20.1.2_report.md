# Comparison Report: GCC 15.0.0 (Release_O3) vs CLANG 20.1.2 (Release_O3)

Generated on: 2025-04-15 20:58:20

## Table of Contents

1. [Configuration Details](#configuration-details)
2. [Summary of Results](#summary-of-results)
3. [int_addition](#int_addition)
4. [float_addition](#float_addition)
5. [container_push_back](#container_push_back)
6. [Failed Comparisons](#failed-comparisons)

## Summary of Results

| Experiment | CLANG 20.1.2 (Release_O3) Improvement (%) | Best Contender |
| ---------- | ----------------------------------------- | -------------- |
| int_addition | <span style='color:red'>-0.90%</span> | CLANG 20.1.2 (Release_O3) |
| float_addition | <span style='color:green'>0.23%</span> | CLANG 20.1.2 (Release_O3) |
| container_push_back | <span style='color:red'>-2.74%</span> | CLANG 20.1.2 (Release_O3) |

## Configuration Details

### Baseline: GCC 15.0.0 (Release_O3)
Path: `results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46`

### Contender 1: CLANG 20.1.2 (Release_O3)
Path: `results/darwin-arm64-Apple-M3-Pro/clang-20.1.2/Release_O3/0528a2c3`

## int_addition

### Original Reports and Data

#### Baseline
- [Report](../gcc-15.0.0/Release_O3/26359d46/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/int_addition)

#### Contender 1: CLANG 20.1.2 (Release_O3)
- [Report](../clang-20.1.2/Release_O3/0528a2c3/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-20.1.2/Release_O3/0528a2c3/int_addition)

### Configuration Comparison: Baseline vs CLANG 20.1.2 (Release_O3)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| **Compiler** | gcc | clang |
| **Compiler Version** | 15.0.0 | 20.1.2 |
| Build Flags | Release_O3 | Release_O3 |
| **Date** | 2025-04-15T14:21:20.416727 | 2025-04-15T16:16:11.902987 |


### Benchmark Comparison: Baseline vs CLANG 20.1.2 (Release_O3)

| Benchmark | GCC 15.0.0 (Release_O3) Time (ns) | CLANG 20.1.2 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Release_O3) CPU (ns) | CLANG 20.1.2 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Release_O3) Iterations | CLANG 20.1.2 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Release_O3) Repetitions | CLANG 20.1.2 (Release_O3) Repetitions | Improvement (%) | GCC 15.0.0 (Release_O3) Threads | CLANG 20.1.2 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ----------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ----------------------------------- | ------------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | ------ |
| BM_IntAddition | 0.28 | 0.28 | <span style='color:red'>-0.90%</span> | 0.28 | 0.28 | <span style='color:red'>-0.85%</span> | 1000000000 | 1000000000 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | tie |


## float_addition

### Original Reports and Data

#### Baseline
- [Report](../gcc-15.0.0/Release_O3/26359d46/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/float_addition)

#### Contender 1: CLANG 20.1.2 (Release_O3)
- [Report](../clang-20.1.2/Release_O3/0528a2c3/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-20.1.2/Release_O3/0528a2c3/float_addition)

### Configuration Comparison: Baseline vs CLANG 20.1.2 (Release_O3)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| **Compiler** | gcc | clang |
| **Compiler Version** | 15.0.0 | 20.1.2 |
| Build Flags | Release_O3 | Release_O3 |
| **Date** | 2025-04-15T14:21:21.903827 | 2025-04-15T16:16:13.399620 |


### Benchmark Comparison: Baseline vs CLANG 20.1.2 (Release_O3)

| Benchmark | GCC 15.0.0 (Release_O3) Time (ns) | CLANG 20.1.2 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Release_O3) CPU (ns) | CLANG 20.1.2 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Release_O3) Iterations | CLANG 20.1.2 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Release_O3) Repetitions | CLANG 20.1.2 (Release_O3) Repetitions | Improvement (%) | GCC 15.0.0 (Release_O3) Threads | CLANG 20.1.2 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ----------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ----------------------------------- | ------------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | ------ |
| BM_FloatAddition | 0.27 | 0.27 | <span style='color:green'>0.23%</span> | 0.27 | 0.27 | <span style='color:green'>0.24%</span> | 1000000000 | 1000000000 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | tie |


## container_push_back

### Original Reports and Data

#### Baseline
- [Report](../gcc-15.0.0/Release_O3/26359d46/container_push_back/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/container_push_back)

#### Contender 1: CLANG 20.1.2 (Release_O3)
- [Report](../clang-20.1.2/Release_O3/0528a2c3/container_push_back/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-20.1.2/Release_O3/0528a2c3/container_push_back)

### Configuration Comparison: Baseline vs CLANG 20.1.2 (Release_O3)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| **Compiler** | gcc | clang |
| **Compiler Version** | 15.0.0 | 20.1.2 |
| Build Flags | Release_O3 | Release_O3 |
| **Date** | 2025-04-15T20:56:38.811726 | 2025-04-15T20:55:22.686536 |


### Benchmark Comparison: Baseline vs CLANG 20.1.2 (Release_O3)

| Benchmark | GCC 15.0.0 (Release_O3) Time (ns) | CLANG 20.1.2 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Release_O3) CPU (ns) | CLANG 20.1.2 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Release_O3) Iterations | CLANG 20.1.2 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Release_O3) Bytes/Second | CLANG 20.1.2 (Release_O3) Bytes/Second | Improvement (%) | GCC 15.0.0 (Release_O3) Items/Second | CLANG 20.1.2 (Release_O3) Items/Second | Improvement (%) | GCC 15.0.0 (Release_O3) Repetitions | CLANG 20.1.2 (Release_O3) Repetitions | Improvement (%) | GCC 15.0.0 (Release_O3) Threads | CLANG 20.1.2 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ----------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ------------------------------------ | -------------------------------------- | --------------- | ------------------------------------ | -------------------------------------- | --------------- | ----------------------------------- | ------------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | ------ |
| BM_ContainerPushBack<std::deque<int>>/1024 | 1.19 | 1.25 | <span style='color:red'>-5.37%</span> | 1.19 | 1.26 | <span style='color:red'>-5.42%</span> | 593502 | 552421 | <span style='color:red'>-6.92%</span> | 3436782709.38 | 3259994317.71 | <span style='color:red'>-5.14%</span> | 859195677.34 | 814998579.43 | <span style='color:red'>-5.14%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::deque<int>>/262144 | 190.37 | 168.89 | <span style='color:green'>11.28%</span> | 177.23 | 168.85 | <span style='color:green'>4.73%</span> | 3954 | 4075 | <span style='color:green'>3.06%</span> | 5916600315.09 | 6210101385.92 | <span style='color:green'>4.96%</span> | 1479150078.77 | 1552525346.48 | <span style='color:green'>4.96%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 20.1.2 (Release_O3) |
| BM_ContainerPushBack<std::deque<int>>/32768 | 23.23 | 22.36 | <span style='color:green'>3.76%</span> | 21.69 | 22.30 | <span style='color:red'>-2.82%</span> | 29097 | 26992 | <span style='color:red'>-7.23%</span> | 6043772853.90 | 5877791201.00 | <span style='color:red'>-2.75%</span> | 1510943213.48 | 1469447800.25 | <span style='color:red'>-2.75%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 20.1.2 (Release_O3) |
| BM_ContainerPushBack<std::deque<int>>/4096 | 3.16 | 3.32 | <span style='color:red'>-5.05%</span> | 3.16 | 3.32 | <span style='color:red'>-5.14%</span> | 221345 | 210078 | <span style='color:red'>-5.09%</span> | 5185597474.20 | 4932266348.73 | <span style='color:red'>-4.89%</span> | 1296399368.55 | 1233066587.18 | <span style='color:red'>-4.89%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::deque<int>>_BigO | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0 | 0 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::deque<int>>_RMS | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0 | 0 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::list<int>>/1024 | 36.13 | 37.17 | <span style='color:red'>-2.90%</span> | 36.10 | 37.16 | <span style='color:red'>-2.94%</span> | 19886 | 18880 | <span style='color:red'>-5.06%</span> | 113466492.07 | 110220990.77 | <span style='color:red'>-2.86%</span> | 28366623.02 | 27555247.69 | <span style='color:red'>-2.86%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::list<int>>/262144 | 11117.85 | 11270.94 | <span style='color:red'>-1.38%</span> | 10768.86 | 11225.98 | <span style='color:red'>-4.24%</span> | 66 | 62 | <span style='color:red'>-6.06%</span> | 97371090.90 | 93406155.94 | <span style='color:red'>-4.07%</span> | 24342772.72 | 23351538.98 | <span style='color:red'>-4.07%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::list<int>>/32768 | 1425.54 | 1483.52 | <span style='color:red'>-4.07%</span> | 1403.65 | 1483.11 | <span style='color:red'>-5.66%</span> | 494 | 463 | <span style='color:red'>-6.28%</span> | 93379417.16 | 88376314.47 | <span style='color:red'>-5.36%</span> | 23344854.29 | 22094078.62 | <span style='color:red'>-5.36%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::list<int>>/4096 | 138.25 | 147.06 | <span style='color:red'>-6.37%</span> | 138.25 | 147.06 | <span style='color:red'>-6.37%</span> | 5006 | 4805 | <span style='color:red'>-4.02%</span> | 118510887.56 | 111413351.75 | <span style='color:red'>-5.99%</span> | 29627721.89 | 27853337.94 | <span style='color:red'>-5.99%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::list<int>>_BigO | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0 | 0 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::list<int>>_RMS | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0 | 0 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>/1024 | 1.33 | 1.31 | <span style='color:green'>1.54%</span> | 1.32 | 1.31 | <span style='color:green'>1.28%</span> | 534653 | 511188 | <span style='color:red'>-4.39%</span> | 3093221119.24 | 3133438161.08 | <span style='color:green'>1.30%</span> | 773305279.81 | 783359540.27 | <span style='color:green'>1.30%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 20.1.2 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>/262144 | 138.72 | 153.69 | <span style='color:red'>-10.79%</span> | 138.69 | 152.99 | <span style='color:red'>-10.31%</span> | 4575 | 4382 | <span style='color:red'>-4.22%</span> | 7560523300.62 | 6854061519.87 | <span style='color:red'>-9.34%</span> | 1890130825.16 | 1713515379.97 | <span style='color:red'>-9.34%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>/32768 | 12.15 | 13.07 | <span style='color:red'>-7.61%</span> | 12.15 | 13.01 | <span style='color:red'>-7.03%</span> | 58615 | 54434 | <span style='color:red'>-7.13%</span> | 10786171861.95 | 10077548384.36 | <span style='color:red'>-6.57%</span> | 2696542965.49 | 2519387096.09 | <span style='color:red'>-6.57%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>/4096 | 2.35 | 2.49 | <span style='color:red'>-5.91%</span> | 2.35 | 2.48 | <span style='color:red'>-5.72%</span> | 291146 | 278480 | <span style='color:red'>-4.35%</span> | 6971365696.89 | 6594052742.41 | <span style='color:red'>-5.41%</span> | 1742841424.22 | 1648513185.60 | <span style='color:red'>-5.41%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>_BigO | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0 | 0 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>_RMS | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0 | 0 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [0, 66, 494, 3954, 4575, 5006, 19886, 29097, 58615, 221345, 291146, 534653, 593502], Contender: [0, 62, 463, 4075, 4382, 4805, 18880, 26992, 54434, 210078, 278480, 511188, 552421]


