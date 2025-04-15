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