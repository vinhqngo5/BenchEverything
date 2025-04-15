# Integer Addition Benchmark

This benchmark measures the performance of simple integer addition operations.

## Configuration

- Compiler: 19.1.7
- Flags: `-std=c++20`
- Platform: linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4
- CPU: Intel-R-Xeon-R-CPU-E5-2695-v4

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Repetitions | Threads | 
| --------- | --------- | -------- | ---------- | ----------- | ------- | 
| BM_IntAddition | 0.39 | 0.39 | 1000000000 | 1 | 1 | 


{{GBENCH_CONSOLE_OUTPUT}}

## Assembly Code

```asm
// Source code for BM_IntAddition (manually added):
static void BM_IntAddition(benchmark::State& state) {
  // Setup
  int a = 42;
  int b = 24;
  int result = 0;
  
  // Benchmark loop
  for (auto _ : state) {
    // This is the operation we're benchmarking
    result = a + b;
    
    // Prevent compiler from optimizing away the result
    benchmark::DoNotOptimize(result);
  }
}

// Assembly:
    6930:	lea    0xfb9(%rip),%rax        # 78f0 <BM_IntAddition(benchmark::State&)>
    6937:	mov    %rax,0xe0(%rbx)
    693e:	xor    %ebp,%ebp
    6940:	mov    %rbx,%rdi
00000000000078f0 <BM_IntAddition(benchmark::State&)>:
    78f0:	push   %rbp
    78f1:	push   %r14
    78f3:	push   %rbx
    78f4:	sub    $0x10,%rsp
    78f8:	mov    %rdi,%rbx
    78fb:	movl   $0x0,0xc(%rsp)
    7903:	mov    0x1c(%rdi),%ebp
    7906:	mov    0x10(%rdi),%r14
    7911:	jne    792d <BM_IntAddition(benchmark::State&)+0x3d>
    7913:	test   %r14,%r14
    7916:	je     792d <BM_IntAddition(benchmark::State&)+0x3d>
    7918:	nopl   0x0(%rax,%rax,1)
    7920:	movl   $0x42,0xc(%rsp)
    7928:	dec    %r14
    792b:	jne    7920 <BM_IntAddition(benchmark::State&)+0x30>
    792d:	mov    %rbx,%rdi
```

## Performance Counters

# started on Tue Apr 15 14:32:50 2025


 Performance counter stats for '/home/vinh/Q22025/BenchEverything/build/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/clang-19.1.7/Release_O3/experiments/int_addition/int_addition_benchmark --benchmark_format=json --benchmark_out=/home/vinh/Q22025/BenchEverything/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/clang-19.1.7/Release_O3/441eb0ef/int_addition/benchmark_output.json':

     1,123,240,575      cycles                                                                
     3,349,927,835      instructions                     #    2.98  insn per cycle            
     1,114,805,927      branch-instructions                                                   
            57,130      branch-misses                    #    0.01% of all branches           

       0.437166326 seconds time elapsed

       0.433179000 seconds user
       0.004001000 seconds sys




## Related Resources

- [Experiment Source Code](/experiments/int_addition)
- [Raw Benchmark Results](/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/clang-19.1.7/Release_O3/441eb0ef/int_addition)
