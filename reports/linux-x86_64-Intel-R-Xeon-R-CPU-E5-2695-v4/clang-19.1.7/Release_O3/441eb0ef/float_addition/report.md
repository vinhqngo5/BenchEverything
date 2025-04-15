# Float Addition Benchmark

This benchmark measures the performance of simple floating-point addition operations.

## Configuration

- Compiler: clang 19.1.7
- Flags: `-std=c++20`
- Platform: linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4
- CPU: Intel-R-Xeon-R-CPU-E5-2695-v4
- Build Flags: Release_O3
- Metadata Hash: 441eb0ef

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Repetitions | Threads | 
| --------- | --------- | -------- | ---------- | ----------- | ------- | 
| BM_FloatAddition | 0.39 | 0.39 | 1000000000 | 1 | 1 | 


## Assembly Code

```asm
// Source code for BM_FloatAddition (manually added):
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

// Assembly:
    692e:	lea    0xfbb(%rip),%rax        # 78f0 <BM_FloatAddition(benchmark::State&)>
    6935:	mov    %rax,0xe0(%rbx)
    693c:	xor    %ebp,%ebp
    693e:	mov    %rbx,%rdi
00000000000078f0 <BM_FloatAddition(benchmark::State&)>:
    78f0:	push   %rbp
    78f1:	push   %r14
    78f3:	push   %rbx
    78f4:	sub    $0x10,%rsp
    78f8:	mov    %rdi,%rbx
    78fb:	movl   $0x0,0xc(%rsp)
    7903:	mov    0x1c(%rdi),%ebp
    7906:	mov    0x10(%rdi),%r14
    7911:	jne    792d <BM_FloatAddition(benchmark::State&)+0x3d>
    7913:	test   %r14,%r14
    7916:	je     792d <BM_FloatAddition(benchmark::State&)+0x3d>
    7918:	nopl   0x0(%rax,%rax,1)
    7920:	movl   $0x42840000,0xc(%rsp)
    7928:	dec    %r14
    792b:	jne    7920 <BM_FloatAddition(benchmark::State&)+0x30>
    792d:	mov    %rbx,%rdi
```

## Performance Counters

# started on Tue Apr 15 14:32:51 2025


 Performance counter stats for '/home/vinh/Q22025/BenchEverything/build/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/clang-19.1.7/Release_O3/experiments/float_addition/float_addition_benchmark --benchmark_format=json --benchmark_out=/home/vinh/Q22025/BenchEverything/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/clang-19.1.7/Release_O3/441eb0ef/float_addition/benchmark_output.json':

     1,122,903,908      cycles                                                                
     3,349,901,083      instructions                     #    2.98  insn per cycle            
     1,114,798,343      branch-instructions                                                   
            56,993      branch-misses                    #    0.01% of all branches           

       0.433577050 seconds time elapsed

       0.427613000 seconds user
       0.005994000 seconds sys




## Related Resources

- [Experiment Source Code](/experiments/float_addition)
- [Raw Benchmark Results](/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/clang-19.1.7/Release_O3/441eb0ef/float_addition)
