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