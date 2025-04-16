// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>> (matched on 'BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>')
0000000100003e8c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003e8c:     	sub	sp, sp, #144
100003e90:     	stp	x26, x25, [sp, #64]
100003e94:     	stp	x24, x23, [sp, #80]
100003e98:     	stp	x22, x21, [sp, #96]
100003e9c:     	stp	x20, x19, [sp, #112]
100003ea0:     	stp	x29, x30, [sp, #128]
100003ea4:     	add	x29, sp, #128
100003ea8:     	mov	x19, x0
;     return this->__begin_[__n];
100003eac:     	ldr	x8, [x0, #32]
;     return range_[pos];
100003eb0:     	ldr	x20, [x8]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
100003eb4:     	ldr	w22, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100003eb8:     	ldr	x21, [x0, #16]
;   StartKeepRunning();
100003ebc:     	bl	0x100005d98 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100003ec0:     	cmp	w22, #0
100003ec4:     	ccmp	x21, #0, #4, eq
100003ecc:     	add	x22, sp, #32
;     --cached_;
100003ed4:     	subs	x21, x21, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
;         state.PauseTiming();
100003edc:     	mov	x0, x19
100003ee0:     	bl	0x100005608 <benchmark::State::PauseTiming()>
;     __list_node_base() : __prev_(_NodeTraits::__unsafe_link_pointer_cast(__self())),
100003ee4:     	stp	x22, x22, [sp, #32]
;   explicit __compressed_pair_elem(_Up&& __u) : __value_(std::forward<_Up>(__u)) {}
100003ee8:     	str	xzr, [sp, #48]
;         state.ResumeTiming();
100003eec:     	mov	x0, x19
100003ef0:     	bl	0x100005b10 <benchmark::State::ResumeTiming()>
100003ef4:     	ldr	x24, [sp, #32]
100003ef8:     	ldr	x23, [sp, #48]
;         for (int i = 0; i < N; ++i) {
100003efc:     	cmp	w20, #1
100003f04:     	mov	x25, #0
;   return __builtin_operator_new(__args...);
100003f08:     	mov	w0, #24
100003f0c:     	bl	0x10002ed9c <_vsnprintf+0x10002ed9c>
;   return ::new (std::__voidify(*__location)) _Tp(std::forward<_Args>(__args)...);
100003f10:     	str	w25, [x0, #16]
;     __l->__next_ = base::__end_as_link();
100003f14:     	stp	x24, x22, [x0]
;     __f->__prev_->__next_ = __f;
100003f18:     	str	x0, [x24, #8]
;     ++base::__sz();
100003f1c:     	add	x8, x23, x25
100003f20:     	add	x8, x8, #1
;     base::__end_.__prev_ = __l;
100003f24:     	str	x0, [sp, #32]
;     ++base::__sz();
100003f28:     	str	x8, [sp, #48]
;         for (int i = 0; i < N; ++i) {
100003f2c:     	add	x25, x25, #1
100003f30:     	mov	x24, x0
;         for (int i = 0; i < N; ++i) {
100003f34:     	cmp	w20, w25
;     bool empty() const _NOEXCEPT {return __sz() == 0;}
100003f3c:     	add	x23, x23, x25
100003f40:     	mov	x24, x0
;     if (!empty())
;         __link_pointer __f = __end_.__next_;
100003f48:     	ldr	x0, [sp, #40]
;     __f->__prev_->__next_ = __l->__next_;
100003f4c:     	ldr	x8, [x24, #8]
100003f50:     	ldr	x9, [x0]
100003f54:     	str	x8, [x9, #8]
;     __l->__next_->__prev_ = __f->__prev_;
100003f58:     	ldr	x8, [x24, #8]
100003f5c:     	str	x9, [x8]
;         __sz() = 0;
100003f60:     	str	xzr, [sp, #48]
;         while (__f != __l)
100003f64:     	cmp	x0, x22
;             __f = __f->__next_;
100003f6c:     	ldr	x23, [x0, #8]
;   __builtin_operator_delete(__args...);
100003f70:     	bl	0x10002ed84 <_vsnprintf+0x10002ed84>
100003f74:     	mov	x0, x23
;         while (__f != __l)
100003f78:     	cmp	x23, x22
;     parent_->FinishKeepRunning();
100003f84:     	mov	x0, x19
100003f88:     	bl	0x100005e30 <benchmark::State::FinishKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(!started_, false)) {
100003f8c:     	ldrb	w8, [x19, #24]
;     return max_iterations - total_iterations_ + batch_leftover_;
100003f94:     	ldp	x10, x8, [x19, #8]
100003f98:     	ldr	x9, [x19]
100003f9c:     	sub	x8, x8, x9
100003fa0:     	add	x23, x8, x10
;     counters["items_per_second"] =
100003fa4:     	add	x21, x19, #64
100003fa8:     	mov	w8, #16