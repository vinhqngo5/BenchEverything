# Integer Addition Benchmark

This benchmark measures the performance of simple integer addition operations.

## Configuration

- Compiler: 14.2.1
- Flags: `-std=c++20`
- Platform: linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4
- CPU: Intel-R-Xeon-R-CPU-E5-2695-v4

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Repetitions | Threads | 
| --------- | --------- | -------- | ---------- | ----------- | ------- | 
| BM_IntAddition | 0.19 | 0.19 | 1000000000 | 1 | 1 | 


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
0000000000408e70 <BM_IntAddition(benchmark::State&)>:
  408e70:	push   %rbp
  408e71:	mov    %rdi,%rbp
  408e74:	push   %rbx
  408e75:	sub    $0x18,%rsp
  408e79:	mov    0x1c(%rdi),%eax
  408e7c:	test   %eax,%eax
  408e7e:	je     408e98 <BM_IntAddition(benchmark::State&)+0x28>
  408ea4:	je     408e85 <BM_IntAddition(benchmark::State&)+0x15>
  408ea6:	mov    %rbx,%rax
  408ea9:	lea    -0x1(%rbx),%rdx
  408ead:	test   $0x1,%bl
  408eb0:	je     408ec0 <BM_IntAddition(benchmark::State&)+0x50>
  408eb2:	mov    %rdx,%rax
  408eb5:	test   %rdx,%rdx
  408eb8:	je     408e85 <BM_IntAddition(benchmark::State&)+0x15>
  408eba:	nopw   0x0(%rax,%rax,1)
  408ec0:	sub    $0x2,%rax
  408ec4:	jne    408ec0 <BM_IntAddition(benchmark::State&)+0x50>
  408ec6:	add    $0x18,%rsp
  408eca:	mov    %rbp,%rdi
  408ecd:	pop    %rbx
  408ece:	pop    %rbp
```

## Performance Counters

# started on Tue Apr 15 14:32:31 2025


 Performance counter stats for '/home/vinh/Q22025/BenchEverything/build/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/gcc-14.2.1/Release_O3/experiments/int_addition/int_addition_benchmark --benchmark_format=json --benchmark_out=/home/vinh/Q22025/BenchEverything/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/gcc-14.2.1/Release_O3/510141cd/int_addition/benchmark_output.json':

       565,780,915      cycles                                                                
     1,126,892,355      instructions                     #    1.99  insn per cycle            
       559,089,735      branch-instructions                                                   
            51,263      branch-misses                    #    0.01% of all branches           

       0.223009130 seconds time elapsed

       0.220060000 seconds user
       0.003000000 seconds sys




## Related Resources

- [Experiment Source Code](/experiments/int_addition)
- [Raw Benchmark Results](/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/gcc-14.2.1/Release_O3/510141cd/int_addition)
