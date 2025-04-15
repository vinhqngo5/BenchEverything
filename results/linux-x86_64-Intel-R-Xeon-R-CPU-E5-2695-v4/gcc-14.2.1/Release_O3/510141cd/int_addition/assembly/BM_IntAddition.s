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