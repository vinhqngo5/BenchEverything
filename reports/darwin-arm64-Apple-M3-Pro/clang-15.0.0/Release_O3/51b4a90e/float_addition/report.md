# Float Addition Benchmark

This benchmark measures the performance of simple floating-point addition operations.

## Configuration

- Compiler: clang 15.0.0
- Flags: `-std=c++20 -O3`
- Platform: darwin-arm64-Apple-M3-Pro
- CPU: Apple-M3-Pro
- Build Flags: Release_O3
- Metadata Hash: 51b4a90e

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ---- | ------- | ---- |
| BM_FloatAddition | 0.27 | 0.27 | 1000000000 | ns | 1 | 1 |


## Assembly Code

```asm

// Function definition for BM_FloatAddition:
/*
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
*/

// Assembly:
0000000100003448 <BM_FloatAddition(benchmark::State&)>:
100003448:     	sub	sp, sp, #64
10000344c:     	stp	x22, x21, [sp, #16]
100003450:     	stp	x20, x19, [sp, #32]
100003454:     	stp	x29, x30, [sp, #48]
100003458:     	add	x29, sp, #48
10000345c:     	mov	x19, x0
100003460:     	str	wzr, [sp, #12]
100003464:     	ldr	w21, [x0, #28]
100003468:     	ldr	x20, [x0, #16]
10000346c:     	bl	0x1000040c4 <benchmark::State::StartKeepRunning()>
100003470:     	cmp	w21, #0
100003474:     	ccmp	x20, #0, #4, eq
10000347c:     	mov	w8, #1115947008
100003480:     	add	x9, sp, #12
100003484:     	str	w8, [sp, #12]
100003488:     	subs	x20, x20, #1
100003490:     	mov	x0, x19
100003494:     	bl	0x100004170 <benchmark::State::FinishKeepRunning()>
100003498:     	ldp	x29, x30, [sp, #48]
10000349c:     	ldp	x20, x19, [sp, #32]
1000034a0:     	ldp	x22, x21, [sp, #16]
1000034a4:     	add	sp, sp, #64
1000034a8:     	ret


```

## Performance Counters

```
None
```

## Related Resources

- [Experiment Source Code](../../../../../../experiments/float_addition)
- [Raw Benchmark Results](../../../../../../results/darwin-arm64-Apple-M3-Pro/clang-15.0.0/Release_O3/51b4a90e/float_addition)
