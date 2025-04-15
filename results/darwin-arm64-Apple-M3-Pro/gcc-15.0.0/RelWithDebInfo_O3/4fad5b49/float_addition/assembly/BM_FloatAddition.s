0000000100001150 <BM_FloatAddition(benchmark::State&)>:
; static void BM_FloatAddition(benchmark::State& state) {
100001150:     	sub	sp, sp, #64
100001154:     	stp	x22, x21, [sp, #16]
100001158:     	stp	x20, x19, [sp, #32]
10000115c:     	stp	x29, x30, [sp, #48]
100001160:     	add	x29, sp, #48
100001164:     	mov	x19, x0
;   float result = 0.0f;
100001168:     	str	wzr, [sp, #12]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
10000116c:     	ldr	w21, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100001170:     	ldr	x20, [x0, #16]
;   StartKeepRunning();
100001180:     	b.eq	0x100001198 <BM_FloatAddition(benchmark::State&)+0x48>
100001184:     	mov	w8, #1115947008
100001188:     	add	x9, sp, #12
;     result = a + b;
10000118c:     	str	w8, [sp, #12]
;     --cached_;
100001190:     	subs	x20, x20, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100001194:     	b.ne	0x10000118c <BM_FloatAddition(benchmark::State&)+0x3c>
;     parent_->FinishKeepRunning();
100001198:     	mov	x0, x19