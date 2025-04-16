# Float Addition Benchmark

This benchmark measures the performance of simple floating-point addition operations.

## Configuration

- Compiler: gcc 15.0.0
- Flags: `-std=c++20 -O0`
- Platform: darwin-arm64-Apple-M3-Pro
- CPU: Apple-M3-Pro
- Build Flags: Debug_O0
- Metadata Hash: 57ef23de

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ---- | ------- | ---- |
| BM_FloatAddition | 2.22 | 2.22 | 321739970 | ns | 1 | 1 |


## Assembly Code

```asm

// Assembly for benchmark function: BM_FloatAddition
0000000100002978 <BM_FloatAddition(benchmark::State&)>:
100002978:     	sub	sp, sp, #304
10000297c:     	stp	x28, x27, [sp, #272]
100002980:     	stp	x29, x30, [sp, #288]
100002984:     	add	x29, sp, #288
100002988:     	str	x0, [sp, #112]
10000298c:     	mov	w8, #1109917696
;   float a = 42.0f;
100002990:     	str	w8, [sp, #108]
100002994:     	mov	w8, #1103101952
;   float b = 24.0f;
100002998:     	str	w8, [sp, #104]
10000299c:     	mov	w8, #0
;   float result = 0.0f;
1000029a0:     	str	w8, [sp, #100]
;   for (auto _ : state) {
1000029a4:     	ldr	x8, [sp, #112]
1000029a8:     	str	x8, [sp, #88]
1000029ac:     	ldr	x8, [sp, #88]
1000029b0:     	str	x8, [sp, #120]
1000029b4:     	ldr	x8, [sp, #120]
1000029b8:     	add	x9, sp, #128
1000029bc:     	stur	x9, [x29, #-64]
1000029c0:     	stur	x8, [x29, #-72]
1000029c4:     	ldur	x9, [x29, #-64]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
1000029c8:     	ldur	x8, [x29, #-72]
1000029cc:     	stur	x9, [x29, #-48]
1000029d0:     	stur	x8, [x29, #-56]
1000029d4:     	ldur	x8, [x29, #-48]
1000029d8:     	mov	x9, x8
1000029dc:     	str	x9, [sp, #32]
1000029e0:     	stur	x8, [x29, #-40]
1000029e4:     	ldur	x0, [x29, #-56]
1000029e8:     	bl	0x10007efcc <_vsnprintf+0x10007efcc>
1000029f4:     	mov	x8, #0
1000029f8:     	str	x8, [sp, #24]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100002a00:     	ldur	x8, [x29, #-56]
100002a04:     	ldr	x8, [x8, #16]
100002a08:     	str	x8, [sp, #24]
100002a10:     	ldr	x9, [sp, #32]
100002a14:     	ldr	x8, [sp, #24]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100002a18:     	str	x8, [x9]
100002a1c:     	ldur	x8, [x29, #-56]
100002a20:     	str	x8, [x9, #8]
;   return StateIterator(this);
100002a24:     	ldr	x8, [sp, #128]
100002a28:     	ldr	x9, [sp, #136]
;   for (auto _ : state) {
100002a2c:     	str	x9, [sp, #80]
100002a30:     	str	x8, [sp, #72]
100002a34:     	ldr	x8, [sp, #88]
100002a38:     	str	x8, [sp, #144]
100002a3c:     	ldr	x0, [sp, #144]
;   StartKeepRunning();
100002a40:     	bl	0x1000045ec <benchmark::State::StartKeepRunning()>
100002a44:     	sub	x8, x29, #136
100002a48:     	stur	x8, [x29, #-32]
100002a4c:     	ldur	x8, [x29, #-32]
100002a50:     	stur	x8, [x29, #-24]
100002a54:     	ldur	x9, [x29, #-24]
100002a58:     	mov	x8, #0
;   StateIterator() : cached_(0), parent_() {}
100002a5c:     	str	x8, [x9]
100002a60:     	str	x8, [x9, #8]
;   return StateIterator();
100002a64:     	ldur	x8, [x29, #-136]
100002a68:     	ldur	x9, [x29, #-128]
;   for (auto _ : state) {
100002a6c:     	str	x9, [sp, #64]
100002a70:     	str	x8, [sp, #56]
100002a78:     	add	x8, sp, #72
100002a7c:     	stur	x8, [x29, #-112]
100002a80:     	add	x8, sp, #56
100002a84:     	stur	x8, [x29, #-120]
100002a88:     	ldur	x8, [x29, #-112]
100002a8c:     	mov	x9, x8
100002a90:     	str	x9, [sp, #16]
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100002a94:     	ldr	x8, [x8]
100002aa0:     	mov	w8, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100002aa4:     	sturb	w8, [x29, #-97]
100002aac:     	ldr	x8, [sp, #16]
;     parent_->FinishKeepRunning();
100002ab0:     	ldr	x0, [x8, #8]
100002ab4:     	bl	0x100004768 <benchmark::State::FinishKeepRunning()>
100002ab8:     	mov	w8, #0
;     return false;
100002abc:     	sturb	w8, [x29, #-97]
;   }
100002ac4:     	ldurb	w8, [x29, #-97]
;   for (auto _ : state) {
100002ac8:     	subs	w8, w8, #1
100002ad4:     	add	x8, sp, #72
100002ad8:     	stur	x8, [x29, #-96]
;     result = a + b;
100002adc:     	ldr	s0, [sp, #108]
100002ae0:     	ldr	s1, [sp, #104]
100002ae4:     	fadd	s0, s0, s1
100002ae8:     	str	s0, [sp, #100]
100002aec:     	add	x8, sp, #100
100002af0:     	stur	x8, [x29, #-88]
;   asm volatile("" : "+r,m"(value) : : "memory");
100002af4:     	ldur	x8, [x29, #-88]
;   for (auto _ : state) {
100002afc:     	add	x8, sp, #72
100002b00:     	stur	x8, [x29, #-80]
100002b04:     	ldur	x8, [x29, #-80]
100002b08:     	mov	x9, x8
100002b0c:     	str	x9, [sp, #8]
;     assert(cached_ > 0);
100002b10:     	ldr	x8, [x8]
100002b14:     	subs	x8, x8, #0

```

## Performance Counters

```
None
```

## Related Resources

- [Experiment Source Code](../../../../../../experiments/float_addition)
- [Raw Benchmark Results](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Debug_O0/57ef23de/float_addition)
