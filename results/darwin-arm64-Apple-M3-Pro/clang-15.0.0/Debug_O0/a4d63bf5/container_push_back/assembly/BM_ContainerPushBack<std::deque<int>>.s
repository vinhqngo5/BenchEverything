// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>> (matched on 'BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>')
0000000100003d20 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003d20:     	stp	x28, x27, [sp, #-32]!
100003d24:     	stp	x29, x30, [sp, #16]
100003d28:     	add	x29, sp, #16
100003d2c:     	sub	sp, sp, #768
100003d30:     	str	x0, [sp, #312]
;     const int N = state.range(0);
100003d34:     	ldr	x8, [sp, #312]
100003d38:     	str	x8, [sp, #328]
100003d3c:     	str	xzr, [sp, #320]
100003d40:     	ldr	x8, [sp, #328]
100003d44:     	str	x8, [sp, #136]
;     assert(range_.size() > pos);
100003d48:     	add	x0, x8, #32