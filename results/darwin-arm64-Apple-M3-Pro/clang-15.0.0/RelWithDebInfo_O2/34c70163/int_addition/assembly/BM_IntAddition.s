// Assembly for benchmark function: BM_IntAddition
0000000100001148 <BM_IntAddition(benchmark::State&)>:
100001148:     	sub	sp, sp, #64
10000114c:     	stp	x22, x21, [sp, #16]
100001150:     	stp	x20, x19, [sp, #32]
100001154:     	stp	x29, x30, [sp, #48]
100001158:     	add	x29, sp, #48
10000115c:     	mov	x19, x0
;   int result = 0;
100001160:     	str	wzr, [sp, #12]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
100001164:     	ldr	w21, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100001168:     	ldr	x20, [x0, #16]
;   StartKeepRunning();
10000116c:     	bl	0x100001d74 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100001170:     	cmp	w21, #0
100001174:     	ccmp	x20, #0, #4, eq
10000117c:     	mov	w8, #66
100001180:     	add	x9, sp, #12
;     result = a + b;
100001184:     	str	w8, [sp, #12]
;     --cached_;
100001188:     	subs	x20, x20, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
;     parent_->FinishKeepRunning();
100001190:     	mov	x0, x19
100001194:     	bl	0x100001e0c <benchmark::State::FinishKeepRunning()>
; }
100001198:     	ldp	x29, x30, [sp, #48]
10000119c:     	ldp	x20, x19, [sp, #32]
1000011a0:     	ldp	x22, x21, [sp, #16]
1000011a4:     	add	sp, sp, #64
1000011a8:     	ret
