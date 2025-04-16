# Multi-Configuration Comparison Report

Generated on: 2025-04-16 17:32:23

## Table of Contents

1. [Configuration Details](#configuration-details)
2. [Summary of Results](#summary-of-results)
3. [int_addition](#int_addition)
4. [float_addition](#float_addition)
5. [container_push_back](#container_push_back)
6. [Failed Comparisons](#failed-comparisons)

## Summary of Results

| Experiment | CLANG 15.0.0 (RelWithDebInfo_O2) Improvement (%) | CLANG 15.0.0 (Release_O3) Improvement (%) | Best Contender |
| ---------- | ------------------------------------------------ | ----------------------------------------- | -------------- |
| int_addition | <span style='color:green'>83.51%</span> | <span style='color:green'>87.24%</span> | CLANG 15.0.0 (Release_O3) |
| float_addition | <span style='color:green'>86.29%</span> | <span style='color:green'>87.65%</span> | CLANG 15.0.0 (Release_O3) |
| container_push_back | <span style='color:green'>96.50%</span> | <span style='color:green'>97.65%</span> | CLANG 15.0.0 (Release_O3) |

## Configuration Details

### Baseline: CLANG 15.0.0 (Debug_O0)
Path: `/Users/vinhq/Library/CloudStorage/OneDrive-Chalmers/Desktop/Q22025/BenchEverything/results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5`

### Contender 1: CLANG 15.0.0 (RelWithDebInfo_O2)
Path: `/Users/vinhq/Library/CloudStorage/OneDrive-Chalmers/Desktop/Q22025/BenchEverything/results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/RelWithDebInfo_O2/34c70163`

### Contender 2: CLANG 15.0.0 (Release_O3)
Path: `/Users/vinhq/Library/CloudStorage/OneDrive-Chalmers/Desktop/Q22025/BenchEverything/results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Release_O3/51b4a90e`

## int_addition

### Original Reports and Data

#### Baseline
- [Report](../clang-15.0.0/Debug_O0/a4d63bf5/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5/int_addition)

#### Contender 1: CLANG 15.0.0 (RelWithDebInfo_O2)
- [Report](../clang-15.0.0/RelWithDebInfo_O2/34c70163/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/RelWithDebInfo_O2/34c70163/int_addition)

### Configuration Comparison: Baseline vs CLANG 15.0.0 (RelWithDebInfo_O2)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| Compiler | clang | clang |
| Compiler Version | 15.0.0 | 15.0.0 |
| **Build Flags** | Debug_O0 | RelWithDebInfo_O2 |
| **Date** | 2025-04-16T17:16:58.158631 | 2025-04-16T17:18:14.975168 |


### Benchmark Comparison: Baseline vs CLANG 15.0.0 (RelWithDebInfo_O2)

| Benchmark | CLANG 15.0.0 (Debug_O0) Time (ns) | CLANG 15.0.0 (RelWithDebInfo_O2) Time (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) CPU (ns) | CLANG 15.0.0 (RelWithDebInfo_O2) CPU (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) Iterations | CLANG 15.0.0 (RelWithDebInfo_O2) Iterations | Improvement (%) | CLANG 15.0.0 (Debug_O0) Repetitions | CLANG 15.0.0 (RelWithDebInfo_O2) Repetitions | Improvement (%) | CLANG 15.0.0 (Debug_O0) Threads | CLANG 15.0.0 (RelWithDebInfo_O2) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ------------------------------------------ | --------------- | -------------------------------- | ----------------------------------------- | --------------- | ---------------------------------- | ------------------------------------------- | --------------- | ----------------------------------- | -------------------------------------------- | --------------- | ------------------------------- | ---------------------------------------- | --------------- | ------ |
| BM_IntAddition | 2.14 | 0.35 | <span style='color:green'>83.51%</span> | 2.13 | 0.31 | <span style='color:green'>85.64%</span> | 321202582 | 1000000000 | <span style='color:green'>211.33%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (RelWithDebInfo_O2) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [321202582], Contender: [1000000000]


#### Contender 2: CLANG 15.0.0 (Release_O3)
- [Report](../clang-15.0.0/Release_O3/51b4a90e/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Release_O3/51b4a90e/int_addition)

### Configuration Comparison: Baseline vs CLANG 15.0.0 (Release_O3)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| Compiler | clang | clang |
| Compiler Version | 15.0.0 | 15.0.0 |
| **Build Flags** | Debug_O0 | Release_O3 |
| **Date** | 2025-04-16T17:16:58.158631 | 2025-04-16T17:15:11.523495 |


### Benchmark Comparison: Baseline vs CLANG 15.0.0 (Release_O3)

| Benchmark | CLANG 15.0.0 (Debug_O0) Time (ns) | CLANG 15.0.0 (Release_O3) Time (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) CPU (ns) | CLANG 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) Iterations | CLANG 15.0.0 (Release_O3) Iterations | Improvement (%) | CLANG 15.0.0 (Debug_O0) Repetitions | CLANG 15.0.0 (Release_O3) Repetitions | Improvement (%) | CLANG 15.0.0 (Debug_O0) Threads | CLANG 15.0.0 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ----------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ----------------------------------- | ------------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | ------ |
| BM_IntAddition | 2.14 | 0.27 | <span style='color:green'>87.24%</span> | 2.13 | 0.27 | <span style='color:green'>87.23%</span> | 321202582 | 1000000000 | <span style='color:green'>211.33%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (Release_O3) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [321202582], Contender: [1000000000]


## float_addition

### Original Reports and Data

#### Baseline
- [Report](../clang-15.0.0/Debug_O0/a4d63bf5/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5/float_addition)

#### Contender 1: CLANG 15.0.0 (RelWithDebInfo_O2)
- [Report](../clang-15.0.0/RelWithDebInfo_O2/34c70163/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/RelWithDebInfo_O2/34c70163/float_addition)

### Configuration Comparison: Baseline vs CLANG 15.0.0 (RelWithDebInfo_O2)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| Compiler | clang | clang |
| Compiler Version | 15.0.0 | 15.0.0 |
| **Build Flags** | Debug_O0 | RelWithDebInfo_O2 |
| **Date** | 2025-04-16T17:17:01.073653 | 2025-04-16T17:18:17.122561 |


### Benchmark Comparison: Baseline vs CLANG 15.0.0 (RelWithDebInfo_O2)

| Benchmark | CLANG 15.0.0 (Debug_O0) Time (ns) | CLANG 15.0.0 (RelWithDebInfo_O2) Time (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) CPU (ns) | CLANG 15.0.0 (RelWithDebInfo_O2) CPU (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) Iterations | CLANG 15.0.0 (RelWithDebInfo_O2) Iterations | Improvement (%) | CLANG 15.0.0 (Debug_O0) Repetitions | CLANG 15.0.0 (RelWithDebInfo_O2) Repetitions | Improvement (%) | CLANG 15.0.0 (Debug_O0) Threads | CLANG 15.0.0 (RelWithDebInfo_O2) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ------------------------------------------ | --------------- | -------------------------------- | ----------------------------------------- | --------------- | ---------------------------------- | ------------------------------------------- | --------------- | ----------------------------------- | -------------------------------------------- | --------------- | ------------------------------- | ---------------------------------------- | --------------- | ------ |
| BM_FloatAddition | 2.20 | 0.30 | <span style='color:green'>86.29%</span> | 2.19 | 0.30 | <span style='color:green'>86.27%</span> | 311947129 | 1000000000 | <span style='color:green'>220.57%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (RelWithDebInfo_O2) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [311947129], Contender: [1000000000]


#### Contender 2: CLANG 15.0.0 (Release_O3)
- [Report](../clang-15.0.0/Release_O3/51b4a90e/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Release_O3/51b4a90e/float_addition)

### Configuration Comparison: Baseline vs CLANG 15.0.0 (Release_O3)

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| Compiler | clang | clang |
| Compiler Version | 15.0.0 | 15.0.0 |
| **Build Flags** | Debug_O0 | Release_O3 |
| **Date** | 2025-04-16T17:17:01.073653 | 2025-04-16T17:15:13.009192 |


### Benchmark Comparison: Baseline vs CLANG 15.0.0 (Release_O3)

| Benchmark | CLANG 15.0.0 (Debug_O0) Time (ns) | CLANG 15.0.0 (Release_O3) Time (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) CPU (ns) | CLANG 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) Iterations | CLANG 15.0.0 (Release_O3) Iterations | Improvement (%) | CLANG 15.0.0 (Debug_O0) Repetitions | CLANG 15.0.0 (Release_O3) Repetitions | Improvement (%) | CLANG 15.0.0 (Debug_O0) Threads | CLANG 15.0.0 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ----------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ----------------------------------- | ------------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | ------ |
| BM_FloatAddition | 2.20 | 0.27 | <span style='color:green'>87.65%</span> | 2.19 | 0.27 | <span style='color:green'>87.64%</span> | 311947129 | 1000000000 | <span style='color:green'>220.57%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (Release_O3) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [311947129], Contender: [1000000000]


## container_push_back

### Original Reports and Data

#### Baseline
- Report: Not available
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Debug_O0/a4d63bf5/container_push_back)

#### Contender 1: CLANG 15.0.0 (RelWithDebInfo_O2)
- [Report](../clang-15.0.0/RelWithDebInfo_O2/34c70163/container_push_back/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/RelWithDebInfo_O2/34c70163/container_push_back)

### Benchmark Comparison: Baseline vs CLANG 15.0.0 (RelWithDebInfo_O2)

| Benchmark | CLANG 15.0.0 (Debug_O0) Time (ns) | CLANG 15.0.0 (RelWithDebInfo_O2) Time (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) CPU (ns) | CLANG 15.0.0 (RelWithDebInfo_O2) CPU (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) Iterations | CLANG 15.0.0 (RelWithDebInfo_O2) Iterations | Improvement (%) | CLANG 15.0.0 (Debug_O0) Bytes/Second | CLANG 15.0.0 (RelWithDebInfo_O2) Bytes/Second | Improvement (%) | CLANG 15.0.0 (Debug_O0) Items/Second | CLANG 15.0.0 (RelWithDebInfo_O2) Items/Second | Improvement (%) | CLANG 15.0.0 (Debug_O0) Repetitions | CLANG 15.0.0 (RelWithDebInfo_O2) Repetitions | Improvement (%) | CLANG 15.0.0 (Debug_O0) Threads | CLANG 15.0.0 (RelWithDebInfo_O2) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ------------------------------------------ | --------------- | -------------------------------- | ----------------------------------------- | --------------- | ---------------------------------- | ------------------------------------------- | --------------- | ------------------------------------ | --------------------------------------------- | --------------- | ------------------------------------ | --------------------------------------------- | --------------- | ----------------------------------- | -------------------------------------------- | --------------- | ------------------------------- | ---------------------------------------- | --------------- | ------ |
| BM_ContainerPushBack<std::vector<int>>/1024 | 34.58 | 1.65 | <span style='color:green'>95.22%</span> | 33.54 | 1.65 | <span style='color:green'>95.07%</span> | 21905 | 443305 | <span style='color:green'>1923.76%</span> | 122128440.37 | 2476662206.49 | <span style='color:green'>1927.92%</span> | 30532110.09 | 619165551.62 | <span style='color:green'>1927.92%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (RelWithDebInfo_O2) |
| BM_ContainerPushBack<std::vector<int>>/32768 | 874.04 | 23.62 | <span style='color:green'>97.30%</span> | 873.95 | 23.58 | <span style='color:green'>97.30%</span> | 770 | 28544 | <span style='color:green'>3607.01%</span> | 149976877.58 | 5558382053.05 | <span style='color:green'>3606.16%</span> | 37494219.40 | 1389595513.26 | <span style='color:green'>3606.16%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (RelWithDebInfo_O2) |
| BM_ContainerPushBack<std::vector<int>>/4096 | 126.98 | 3.81 | <span style='color:green'>97.00%</span> | 124.03 | 3.81 | <span style='color:green'>96.93%</span> | 6028 | 171947 | <span style='color:green'>2752.47%</span> | 132099872.00 | 4300630547.95 | <span style='color:green'>3155.59%</span> | 33024968.00 | 1075157636.99 | <span style='color:green'>3155.59%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (RelWithDebInfo_O2) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [770, 6028, 21905], Contender: [0, 61, 480, 2986, 3738, 4719, 17864, 28544, 31787, 171947, 192887, 443305, 490932]


#### Contender 2: CLANG 15.0.0 (Release_O3)
- [Report](../clang-15.0.0/Release_O3/51b4a90e/container_push_back/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Release_O3/51b4a90e/container_push_back)

### Benchmark Comparison: Baseline vs CLANG 15.0.0 (Release_O3)

| Benchmark | CLANG 15.0.0 (Debug_O0) Time (ns) | CLANG 15.0.0 (Release_O3) Time (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) CPU (ns) | CLANG 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | CLANG 15.0.0 (Debug_O0) Iterations | CLANG 15.0.0 (Release_O3) Iterations | Improvement (%) | CLANG 15.0.0 (Debug_O0) Bytes/Second | CLANG 15.0.0 (Release_O3) Bytes/Second | Improvement (%) | CLANG 15.0.0 (Debug_O0) Items/Second | CLANG 15.0.0 (Release_O3) Items/Second | Improvement (%) | CLANG 15.0.0 (Debug_O0) Repetitions | CLANG 15.0.0 (Release_O3) Repetitions | Improvement (%) | CLANG 15.0.0 (Debug_O0) Threads | CLANG 15.0.0 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | --------------------------------- | ----------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ------------------------------------ | -------------------------------------- | --------------- | ------------------------------------ | -------------------------------------- | --------------- | ----------------------------------- | ------------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | ------ |
| BM_ContainerPushBack<std::vector<int>>/1024 | 34.58 | 1.28 | <span style='color:green'>96.29%</span> | 33.54 | 1.28 | <span style='color:green'>96.18%</span> | 21905 | 554618 | <span style='color:green'>2431.92%</span> | 122128440.37 | 3195489923.52 | <span style='color:green'>2516.50%</span> | 30532110.09 | 798872480.88 | <span style='color:green'>2516.50%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>/32768 | 874.04 | 12.54 | <span style='color:green'>98.57%</span> | 873.95 | 12.54 | <span style='color:green'>98.57%</span> | 770 | 55907 | <span style='color:green'>7160.65%</span> | 149976877.58 | 10456052817.90 | <span style='color:green'>6871.78%</span> | 37494219.40 | 2614013204.48 | <span style='color:green'>6871.78%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (Release_O3) |
| BM_ContainerPushBack<std::vector<int>>/4096 | 126.98 | 2.41 | <span style='color:green'>98.10%</span> | 124.03 | 2.41 | <span style='color:green'>98.05%</span> | 6028 | 295110 | <span style='color:green'>4795.65%</span> | 132099872.00 | 6786156532.28 | <span style='color:green'>5037.14%</span> | 33024968.00 | 1696539133.07 | <span style='color:green'>5037.14%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | CLANG 15.0.0 (Release_O3) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [770, 6028, 21905], Contender: [0, 67, 469, 4383, 4478, 4978, 19790, 33184, 55907, 200640, 295110, 554618, 568768]


