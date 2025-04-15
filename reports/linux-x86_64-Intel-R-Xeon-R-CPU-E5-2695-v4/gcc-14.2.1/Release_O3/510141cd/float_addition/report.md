# Float Addition Benchmark

This benchmark measures the performance of simple floating-point addition operations.

## Configuration

- Compiler: gcc 14.2.1
- Flags: `-std=c++20`
- Platform: linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4
- CPU: Intel-R-Xeon-R-CPU-E5-2695-v4
- Build Flags: Release_O3
- Metadata Hash: 510141cd

## Benchmark Results

| Benchmark | Time (ns) | CPU (ns) | Iterations | Repetitions | Threads | 
| --------- | --------- | -------- | ---------- | ----------- | ------- | 
| BM_FloatAddition | 0.19 | 0.19 | 1000000000 | 1 | 1 | 


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
0000000000408e80 <BM_FloatAddition(benchmark::State&)>:
  408e80:	push   %rbp
  408e81:	mov    %rdi,%rbp
  408e84:	push   %rbx
  408e85:	sub    $0x18,%rsp
  408e89:	mov    0x1c(%rdi),%eax
  408e8c:	test   %eax,%eax
  408e8e:	je     408ea8 <BM_FloatAddition(benchmark::State&)+0x28>
  408eb4:	je     408e95 <BM_FloatAddition(benchmark::State&)+0x15>
  408eb6:	mov    %rbx,%rax
  408eb9:	lea    -0x1(%rbx),%rdx
  408ebd:	test   $0x1,%bl
  408ec0:	je     408ed0 <BM_FloatAddition(benchmark::State&)+0x50>
  408ec2:	mov    %rdx,%rax
  408ec5:	test   %rdx,%rdx
  408ec8:	je     408e95 <BM_FloatAddition(benchmark::State&)+0x15>
  408eca:	nopw   0x0(%rax,%rax,1)
  408ed0:	sub    $0x2,%rax
  408ed4:	jne    408ed0 <BM_FloatAddition(benchmark::State&)+0x50>
  408ed6:	add    $0x18,%rsp
  408eda:	mov    %rbp,%rdi
  408edd:	pop    %rbx
  408ede:	pop    %rbp
```

## Performance Counters

```
# started on Tue Apr 15 14:32:31 2025


 Performance counter stats for '/home/vinh/Q22025/BenchEverything/build/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/gcc-14.2.1/Release_O3/experiments/float_addition/float_addition_benchmark --benchmark_format=json --benchmark_out=/home/vinh/Q22025/BenchEverything/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/gcc-14.2.1/Release_O3/510141cd/float_addition/benchmark_output.json':

       566,075,400      cycles                                                                
     1,126,939,319      instructions                     #    1.99  insn per cycle            
       559,097,675      branch-instructions                                                   
            50,144      branch-misses                    #    0.01% of all branches           

       0.218827430 seconds time elapsed

       0.215867000 seconds user
       0.002998000 seconds sys



```

## Related Resources

- [Experiment Source Code](/experiments/float_addition)
- [Raw Benchmark Results](/results/linux-x86_64-Intel-R-Xeon-R-CPU-E5-2695-v4/gcc-14.2.1/Release_O3/510141cd/float_addition)
