// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>> (matched on 'BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>')
00000001000036a8 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
1000036a8:     	sub	sp, sp, #160
1000036ac:     	stp	x28, x27, [sp, #64]
1000036b0:     	stp	x26, x25, [sp, #80]
1000036b4:     	stp	x24, x23, [sp, #96]
1000036b8:     	stp	x22, x21, [sp, #112]
1000036bc:     	stp	x20, x19, [sp, #128]
1000036c0:     	stp	x29, x30, [sp, #144]
1000036c4:     	add	x29, sp, #144
1000036c8:     	mov	x23, x0
;     return this->__begin_[__n];
1000036cc:     	ldr	x8, [x0, #32]
;     return range_[pos];
1000036d0:     	ldr	x20, [x8]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
1000036d4:     	ldr	w19, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
1000036d8:     	ldr	x22, [x0, #16]
;   StartKeepRunning();
1000036dc:     	bl	0x100005d98 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
1000036e0:     	cmp	w19, #0
1000036e4:     	ccmp	x22, #0, #4, eq
1000036ec:     	str	x23, [sp]
;     --cached_;
1000036f4:     	subs	x22, x22, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
;         state.PauseTiming();
1000036fc:     	mov	x0, x23
100003700:     	bl	0x100005608 <benchmark::State::PauseTiming()>
;     pointer __end_ = nullptr;
100003704:     	stp	xzr, xzr, [sp, #32]
100003708:     	str	xzr, [sp, #48]
;         state.ResumeTiming();
10000370c:     	mov	x0, x23
100003710:     	bl	0x100005b10 <benchmark::State::ResumeTiming()>
;         for (int i = 0; i < N; ++i) {
100003714:     	cmp	w20, #1
10000371c:     	mov	x21, #0
100003720:     	mov	x27, #0
100003724:     	mov	x23, #0
100003728:     	mov	w25, #0
10000372c:     	ldr	x26, [sp, #32]
;   return ::new (std::__voidify(*__location)) _Tp(std::forward<_Args>(__args)...);
100003734:     	str	w25, [x27], #4
;       __v_.__end_ = __pos_;
100003738:     	str	x27, [sp, #40]
10000373c:     	mov	x19, x27
;         for (int i = 0; i < N; ++i) {
100003740:     	add	w25, w25, #1
100003744:     	mov	x27, x19
;         for (int i = 0; i < N; ++i) {
100003748:     	cmp	w25, w20
;     if (this->__end_ != this->__end_cap())
100003750:     	cmp	x27, x23
;         {return static_cast<size_type>(this->__end_ - this->__begin_);}
100003758:     	sub	x24, x27, x21
10000375c:     	asr	x23, x24, #2
;     __split_buffer<value_type, allocator_type&> __v(__recommend(size() + 1), size(), __a);
100003760:     	add	x8, x23, #1
;     if (__new_size > __ms)
100003764:     	lsr	x9, x8, #62
;     if (__cap >= __ms / 2)
10000376c:     	asr	x9, x24, #1
100003770:     	cmp	x9, x8
100003774:     	csel	x8, x9, x8, hi
100003778:     	mov	x9, #9223372036854775804
10000377c:     	cmp	x24, x9
100003780:     	mov	x9, #4611686018427387903
100003784:     	csel	x28, x8, x9, lo
;     if (__cap == 0) {