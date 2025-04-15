# Comparison Report: GCC 15.0.0 (Debug_O0) vs GCC 15.0.0 (Release_O3)

Generated on: 2025-04-15 19:38:20

## Table of Contents

1. [Configuration Details](#configuration-details)
2. [Summary of Results](#summary-of-results)
3. [int_addition](#int_addition)
4. [float_addition](#float_addition)
5. [Failed Comparisons](#failed-comparisons)

## Summary of Results

| Experiment | Average Improvement (%) | Number of Benchmarks |
|------------|-------------------------|------------------------|
| int_addition | <span style='color:green'>86.68%</span> | 1 |
| float_addition | <span style='color:green'>86.63%</span> | 1 |

## Configuration Details

### Baseline: GCC 15.0.0 (Debug_O0)
Path: `results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/845f2637`

### Contender: GCC 15.0.0 (Release_O3)
Path: `results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46`

## int_addition

### Configuration Details

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| Compiler | gcc | gcc |
| Compiler Version | 15.0.0 | 15.0.0 |
| **Build Flags** | Debug_O0 | Release_O3 |
| **Date** | 2025-04-15T14:22:13.481128 | 2025-04-15T14:21:20.416727 |


### Original Reports and Data

#### Baseline
- [Report](../gcc-15.0.0/Debug_O0/845f2637/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/845f2637/int_addition)

#### Contender
- [Report](../gcc-15.0.0/Release_O3/26359d46/int_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/int_addition)

### Benchmark Comparison

| Benchmark | GCC 15.0.0 (Debug_O0) Time (ns) | GCC 15.0.0 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) CPU (ns) | GCC 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) Iterations | GCC 15.0.0 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Debug_O0) Repetitions | GCC 15.0.0 (Release_O3) Repetitions | Improvement (%) | GCC 15.0.0 (Debug_O0) Threads | GCC 15.0.0 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | ------------------------------- | --------------------------------- | --------------- | ------------------------------ | -------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | --------------------------------- | ----------------------------------- | --------------- | ----------------------------- | ------------------------------- | --------------- | ------ |
| BM_IntAddition | 2.09 | 0.28 | <span style='color:green'>86.68%</span> | 2.09 | 0.28 | <span style='color:green'>86.68%</span> | 336739210 | 1000000000 | <span style='color:green'>196.97%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [336739210], Contender: [1000000000]


## float_addition

### Configuration Details

| Property | Baseline | Contender |
|----------|----------|----------|
| Platform | darwin-arm64-Apple-M3-Pro | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro | Apple-M3-Pro |
| Compiler | gcc | gcc |
| Compiler Version | 15.0.0 | 15.0.0 |
| **Build Flags** | Debug_O0 | Release_O3 |
| **Date** | 2025-04-15T14:22:16.346071 | 2025-04-15T14:21:21.903827 |


### Original Reports and Data

#### Baseline
- [Report](../gcc-15.0.0/Debug_O0/845f2637/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/845f2637/float_addition)

#### Contender
- [Report](../gcc-15.0.0/Release_O3/26359d46/float_addition/report.md)
- [Raw Results](../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/float_addition)

### Benchmark Comparison

| Benchmark | GCC 15.0.0 (Debug_O0) Time (ns) | GCC 15.0.0 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) CPU (ns) | GCC 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) Iterations | GCC 15.0.0 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Debug_O0) Repetitions | GCC 15.0.0 (Release_O3) Repetitions | Improvement (%) | GCC 15.0.0 (Debug_O0) Threads | GCC 15.0.0 (Release_O3) Threads | Improvement (%) | Winner |
| --------- | ------------------------------- | --------------------------------- | --------------- | ------------------------------ | -------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | --------------------------------- | ----------------------------------- | --------------- | ----------------------------- | ------------------------------- | --------------- | ------ |
| BM_FloatAddition | 2.05 | 0.27 | <span style='color:green'>86.63%</span> | 2.05 | 0.27 | <span style='color:green'>86.63%</span> | 336031184 | 1000000000 | <span style='color:green'>197.59%</span> | 1 | 1 | <span style='color:'>0.00%</span> | 1 | 1 | <span style='color:'>0.00%</span> | GCC 15.0.0 (Release_O3) |

**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:
- **Iterations differ:** Baseline: [336031184], Contender: [1000000000]


