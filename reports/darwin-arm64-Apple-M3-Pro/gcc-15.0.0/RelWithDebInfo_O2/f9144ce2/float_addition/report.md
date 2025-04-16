# Float Addition Benchmark

This benchmark measures the performance of simple floating-point addition operations.

## Configuration

- Compiler: gcc 15.0.0
- Flags: `-std=c++20 -O2`
- Platform: darwin-arm64-Apple-M3-Pro
- CPU: Apple-M3-Pro
- Build Flags: RelWithDebInfo_O2
- Metadata Hash: f9144ce2

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ---- | ------- | ---- |
| BM_FloatAddition | 0.28 | 0.28 | 1000000000 | ns | 1 | 1 |


## Assembly Code

```asm

// Assembly for benchmark function: BM_FloatAddition
0000000100001150 <BM_FloatAddition(benchmark::State&)>:
100001150:     	sub	sp, sp, #64
100001154:     	stp	x22, x21, [sp, #16]
100001158:     	stp	x20, x19, [sp, #32]
10000115c:     	stp	x29, x30, [sp, #48]
100001160:     	add	x29, sp, #48
100001164:     	mov	x19, x0
;   float result = 0.0f;
100001168:     	str	wzr, [sp, #12]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
10000116c:     	ldr	w21, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100001170:     	ldr	x20, [x0, #16]
;   StartKeepRunning();
100001174:     	bl	0x100001d74 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100001178:     	cmp	w21, #0
10000117c:     	ccmp	x20, #0, #4, eq
100001184:     	mov	w8, #1115947008
100001188:     	add	x9, sp, #12
;     result = a + b;
10000118c:     	str	w8, [sp, #12]
;     --cached_;
100001190:     	subs	x20, x20, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
;     parent_->FinishKeepRunning();
100001198:     	mov	x0, x19
10000119c:     	bl	0x100001e0c <benchmark::State::FinishKeepRunning()>
; }
1000011a0:     	ldp	x29, x30, [sp, #48]
1000011a4:     	ldp	x20, x19, [sp, #32]
1000011a8:     	ldp	x22, x21, [sp, #16]
1000011ac:     	add	sp, sp, #64
1000011b0:     	ret


```

## Performance Counters

```
None
```

## Related Resources

- [Experiment Source Code](../../../../../../experiments/float_addition)
- [Raw Benchmark Results](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/RelWithDebInfo_O2/f9144ce2/float_addition)
