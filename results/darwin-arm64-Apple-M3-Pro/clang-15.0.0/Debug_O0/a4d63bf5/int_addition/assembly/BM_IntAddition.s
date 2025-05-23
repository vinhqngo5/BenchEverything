// Assembly for benchmark function: BM_IntAddition
000000010000295c <BM_IntAddition(benchmark::State&)>:
10000295c:     	sub	sp, sp, #304
100002960:     	stp	x28, x27, [sp, #272]
100002964:     	stp	x29, x30, [sp, #288]
100002968:     	add	x29, sp, #288
10000296c:     	str	x0, [sp, #112]
100002970:     	mov	w8, #42
;   int a = 42;
100002974:     	str	w8, [sp, #108]
100002978:     	mov	w8, #24
;   int b = 24;
10000297c:     	str	w8, [sp, #104]
100002980:     	mov	w8, #0
;   int result = 0;
100002984:     	str	w8, [sp, #100]
;   for (auto _ : state) {
100002988:     	ldr	x8, [sp, #112]
10000298c:     	str	x8, [sp, #88]
100002990:     	ldr	x8, [sp, #88]
100002994:     	str	x8, [sp, #120]
100002998:     	ldr	x8, [sp, #120]
10000299c:     	add	x9, sp, #128
1000029a0:     	stur	x9, [x29, #-64]
1000029a4:     	stur	x8, [x29, #-72]
1000029a8:     	ldur	x9, [x29, #-64]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
1000029ac:     	ldur	x8, [x29, #-72]
1000029b0:     	stur	x9, [x29, #-48]
1000029b4:     	stur	x8, [x29, #-56]
1000029b8:     	ldur	x8, [x29, #-48]
1000029bc:     	mov	x9, x8
1000029c0:     	str	x9, [sp, #32]
1000029c4:     	stur	x8, [x29, #-40]
1000029c8:     	ldur	x0, [x29, #-56]
1000029cc:     	bl	0x10007efb0 <_vsnprintf+0x10007efb0>
1000029d8:     	mov	x8, #0
1000029dc:     	str	x8, [sp, #24]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
1000029e4:     	ldur	x8, [x29, #-56]
1000029e8:     	ldr	x8, [x8, #16]
1000029ec:     	str	x8, [sp, #24]
1000029f4:     	ldr	x9, [sp, #32]
1000029f8:     	ldr	x8, [sp, #24]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
1000029fc:     	str	x8, [x9]
100002a00:     	ldur	x8, [x29, #-56]
100002a04:     	str	x8, [x9, #8]
;   return StateIterator(this);
100002a08:     	ldr	x8, [sp, #128]
100002a0c:     	ldr	x9, [sp, #136]
;   for (auto _ : state) {
100002a10:     	str	x9, [sp, #80]
100002a14:     	str	x8, [sp, #72]
100002a18:     	ldr	x8, [sp, #88]
100002a1c:     	str	x8, [sp, #144]
100002a20:     	ldr	x0, [sp, #144]
;   StartKeepRunning();
100002a24:     	bl	0x1000045d0 <benchmark::State::StartKeepRunning()>
100002a28:     	sub	x8, x29, #136
100002a2c:     	stur	x8, [x29, #-32]
100002a30:     	ldur	x8, [x29, #-32]
100002a34:     	stur	x8, [x29, #-24]
100002a38:     	ldur	x9, [x29, #-24]
100002a3c:     	mov	x8, #0
;   StateIterator() : cached_(0), parent_() {}
100002a40:     	str	x8, [x9]
100002a44:     	str	x8, [x9, #8]
;   return StateIterator();
100002a48:     	ldur	x8, [x29, #-136]
100002a4c:     	ldur	x9, [x29, #-128]
;   for (auto _ : state) {
100002a50:     	str	x9, [sp, #64]
100002a54:     	str	x8, [sp, #56]
100002a5c:     	add	x8, sp, #72
100002a60:     	stur	x8, [x29, #-112]
100002a64:     	add	x8, sp, #56
100002a68:     	stur	x8, [x29, #-120]
100002a6c:     	ldur	x8, [x29, #-112]
100002a70:     	mov	x9, x8
100002a74:     	str	x9, [sp, #16]
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100002a78:     	ldr	x8, [x8]
100002a84:     	mov	w8, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100002a88:     	sturb	w8, [x29, #-97]
100002a90:     	ldr	x8, [sp, #16]
;     parent_->FinishKeepRunning();
100002a94:     	ldr	x0, [x8, #8]
100002a98:     	bl	0x10000474c <benchmark::State::FinishKeepRunning()>
100002a9c:     	mov	w8, #0
;     return false;
100002aa0:     	sturb	w8, [x29, #-97]
;   }
100002aa8:     	ldurb	w8, [x29, #-97]
;   for (auto _ : state) {
100002aac:     	subs	w8, w8, #1
100002ab8:     	add	x8, sp, #72
100002abc:     	stur	x8, [x29, #-96]
;     result = a + b;
100002ac0:     	ldr	w8, [sp, #108]
100002ac4:     	ldr	w9, [sp, #104]
100002ac8:     	add	w8, w8, w9
100002acc:     	str	w8, [sp, #100]
100002ad0:     	add	x8, sp, #100
100002ad4:     	stur	x8, [x29, #-88]
;   asm volatile("" : "+r,m"(value) : : "memory");
100002ad8:     	ldur	x8, [x29, #-88]
;   for (auto _ : state) {
100002ae0:     	add	x8, sp, #72
100002ae4:     	stur	x8, [x29, #-80]
100002ae8:     	ldur	x8, [x29, #-80]
100002aec:     	mov	x9, x8
100002af0:     	str	x9, [sp, #8]
;     assert(cached_ > 0);
100002af4:     	ldr	x8, [x8]
100002af8:     	subs	x8, x8, #0