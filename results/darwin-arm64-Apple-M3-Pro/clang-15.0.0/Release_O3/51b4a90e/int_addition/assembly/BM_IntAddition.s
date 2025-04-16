// Function definition for BM_IntAddition:
/*
// Simple integer addition benchmark
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
*/

// Assembly:
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
100003464:     	bl	0x1000040c4 <benchmark::State::StartKeepRunning()>
100003468:     	cmp	w21, #0
10000346c:     	ccmp	x20, #0, #4, eq
100003474:     	mov	w8, #66
100003478:     	add	x9, sp, #12
10000347c:     	str	w8, [sp, #12]
100003480:     	subs	x20, x20, #1
100003488:     	mov	x0, x19
10000348c:     	bl	0x100004170 <benchmark::State::FinishKeepRunning()>
100003490:     	ldp	x29, x30, [sp, #48]
100003494:     	ldp	x20, x19, [sp, #32]
100003498:     	ldp	x22, x21, [sp, #16]
10000349c:     	add	sp, sp, #64
1000034a0:     	ret
