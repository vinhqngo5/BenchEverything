// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>> (matched on 'BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>')
0000000100003d3c <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003d3c:     	stp	x28, x27, [sp, #-32]!
100003d40:     	stp	x29, x30, [sp, #16]
100003d44:     	add	x29, sp, #16
100003d48:     	sub	sp, sp, #768
100003d4c:     	str	x0, [sp, #312]
;     const int N = state.range(0);
100003d50:     	ldr	x8, [sp, #312]
100003d54:     	str	x8, [sp, #328]
100003d58:     	str	xzr, [sp, #320]
100003d5c:     	ldr	x8, [sp, #328]
100003d60:     	str	x8, [sp, #136]
;     assert(range_.size() > pos);
100003d64:     	add	x0, x8, #32