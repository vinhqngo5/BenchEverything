0000000100001148 <BM_IntAddition(benchmark::State&)>:
; static void BM_IntAddition(benchmark::State& state) {
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
100001178:     	b.eq	0x100001190 <BM_IntAddition(benchmark::State&)+0x48>
10000117c:     	mov	w8, #66
100001180:     	add	x9, sp, #12
;     result = a + b;
100001184:     	str	w8, [sp, #12]
;     --cached_;
100001188:     	subs	x20, x20, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
10000118c:     	b.ne	0x100001184 <BM_IntAddition(benchmark::State&)+0x3c>
;     parent_->FinishKeepRunning();
100001190:     	mov	x0, x19