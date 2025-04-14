# Integer Addition Benchmark

This benchmark measures the performance of simple integer addition operations.

## Configuration

- Compiler: Unknown
- Flags: `-std=c++20`
- Platform: darwin-arm64

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations |
|-----------|----------|---------|------------|
| BM_IntAddition | 0.28 | 0.28 | 1000000000 |


## Assembly Code

```asm
0000000100003440 <BM_IntAddition(benchmark::State&)>:
100003440:     	sub	sp, sp, #64
100003444:     	stp	x22, x21, [sp, #16]
100003448:     	stp	x20, x19, [sp, #32]
10000344c:     	stp	x29, x30, [sp, #48]
100003450:     	add	x29, sp, #48
100003454:     	mov	x19, x0
100003458:     	str	wzr, [sp, #12]
10000345c:     	ldr	w21, [x0, #28]
100003460:     	ldr	x20, [x0, #16]
100003470:     	b.eq	0x100003488 <BM_IntAddition(benchmark::State&)+0x48>
100003474:     	mov	w8, #66
100003478:     	add	x9, sp, #12
10000347c:     	str	w8, [sp, #12]
100003480:     	subs	x20, x20, #1
100003484:     	b.ne	0x10000347c <BM_IntAddition(benchmark::State&)+0x3c>
100003488:     	mov	x0, x19
```

## Performance Counters

Performance counter data not available