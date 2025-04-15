# Comparison Report: GCC 15.0.0 (Debug_O0) vs GCC 15.0.0 (Release_O3)

Generated on: 2025-04-15 19:04:28

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


### Original Reports

- [Baseline Report](reports/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/845f2637/int_addition/report.md)
- [Contender Report](reports/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/int_addition/report.md)

### Benchmark Comparison

| Benchmark | GCC 15.0.0 (Debug_O0) CPU (ns) | GCC 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) repetitions | GCC 15.0.0 (Release_O3) repetitions | Improvement (%) | GCC 15.0.0 (Debug_O0) Time (ns) | GCC 15.0.0 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) Iterations | GCC 15.0.0 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Debug_O0) per_family_instance_index | GCC 15.0.0 (Release_O3) per_family_instance_index | Improvement (%) | GCC 15.0.0 (Debug_O0) repetition_index | GCC 15.0.0 (Release_O3) repetition_index | Improvement (%) | GCC 15.0.0 (Debug_O0) threads | GCC 15.0.0 (Release_O3) threads | Improvement (%) | GCC 15.0.0 (Debug_O0) family_index | GCC 15.0.0 (Release_O3) family_index | Improvement (%) | Winner |
| --------- | ------------------------------ | -------------------------------- | --------------- | --------------------------------- | ----------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ----------------------------------------------- | ------------------------------------------------- | --------------- | -------------------------------------- | ---------------------------------------- | --------------- | ----------------------------- | ------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ------ |
| BM_IntAddition | 2.09 | 0.28 | <span style='color:green'>86.68%</span> | 1.00 | 1.00 | <span style='color:'>0.00%</span> | 2.09 | 0.28 | <span style='color:green'>86.68%</span> | 336739210.0 | 1000000000.0 | <span style='color:green'>196.97%</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1.00 | 1.00 | <span style='color:'>0.00%</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | GCC 15.0.0 (Release_O3) |


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


### Original Reports

- [Baseline Report](reports/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/845f2637/float_addition/report.md)
- [Contender Report](reports/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/26359d46/float_addition/report.md)

### Benchmark Comparison

| Benchmark | GCC 15.0.0 (Debug_O0) CPU (ns) | GCC 15.0.0 (Release_O3) CPU (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) repetitions | GCC 15.0.0 (Release_O3) repetitions | Improvement (%) | GCC 15.0.0 (Debug_O0) Time (ns) | GCC 15.0.0 (Release_O3) Time (ns) | Improvement (%) | GCC 15.0.0 (Debug_O0) Iterations | GCC 15.0.0 (Release_O3) Iterations | Improvement (%) | GCC 15.0.0 (Debug_O0) per_family_instance_index | GCC 15.0.0 (Release_O3) per_family_instance_index | Improvement (%) | GCC 15.0.0 (Debug_O0) repetition_index | GCC 15.0.0 (Release_O3) repetition_index | Improvement (%) | GCC 15.0.0 (Debug_O0) threads | GCC 15.0.0 (Release_O3) threads | Improvement (%) | GCC 15.0.0 (Debug_O0) family_index | GCC 15.0.0 (Release_O3) family_index | Improvement (%) | Winner |
| --------- | ------------------------------ | -------------------------------- | --------------- | --------------------------------- | ----------------------------------- | --------------- | ------------------------------- | --------------------------------- | --------------- | -------------------------------- | ---------------------------------- | --------------- | ----------------------------------------------- | ------------------------------------------------- | --------------- | -------------------------------------- | ---------------------------------------- | --------------- | ----------------------------- | ------------------------------- | --------------- | ---------------------------------- | ------------------------------------ | --------------- | ------ |
| BM_FloatAddition | 2.05 | 0.27 | <span style='color:green'>86.63%</span> | 1.00 | 1.00 | <span style='color:'>0.00%</span> | 2.05 | 0.27 | <span style='color:green'>86.63%</span> | 336031184.0 | 1000000000.0 | <span style='color:green'>197.59%</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | 1.00 | 1.00 | <span style='color:'>0.00%</span> | 0.00 | 0.00 | <span style='color:red'>∞</span> | GCC 15.0.0 (Release_O3) |


