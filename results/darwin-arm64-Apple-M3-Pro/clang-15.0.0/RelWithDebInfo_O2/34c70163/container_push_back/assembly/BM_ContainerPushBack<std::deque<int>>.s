// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>> (matched on 'BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>')
0000000100003b04 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003b04:     	sub	sp, sp, #160
100003b08:     	stp	x24, x23, [sp, #96]
100003b0c:     	stp	x22, x21, [sp, #112]
100003b10:     	stp	x20, x19, [sp, #128]
100003b14:     	stp	x29, x30, [sp, #144]
100003b18:     	add	x29, sp, #144
100003b1c:     	mov	x19, x0
;     return this->__begin_[__n];
100003b20:     	ldr	x8, [x0, #32]
;     return range_[pos];
100003b24:     	ldr	x20, [x8]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
100003b28:     	ldr	w22, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100003b2c:     	ldr	x21, [x0, #16]
;   StartKeepRunning();
100003b30:     	bl	0x100005d98 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100003b34:     	cmp	w22, #0
100003b38:     	ccmp	x21, #0, #4, eq
;     parent_->FinishKeepRunning();
100003b40:     	mov	x0, x19
100003b44:     	bl	0x100005e30 <benchmark::State::FinishKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(!started_, false)) {
100003b48:     	ldrb	w8, [x19, #24]
;     return max_iterations - total_iterations_ + batch_leftover_;
100003b50:     	ldp	x10, x8, [x19, #8]
100003b54:     	ldr	x9, [x19]
100003b58:     	sub	x8, x8, x9
100003b5c:     	add	x23, x8, x10
;     counters["items_per_second"] =
100003b60:     	add	x21, x19, #64
100003b64:     	mov	w8, #16