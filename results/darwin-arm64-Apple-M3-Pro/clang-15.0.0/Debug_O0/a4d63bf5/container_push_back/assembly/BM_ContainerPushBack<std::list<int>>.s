// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>> (matched on 'BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>')
00000001000042d8 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
1000042d8:     	stp	x28, x27, [sp, #-32]!
1000042dc:     	stp	x29, x30, [sp, #16]
1000042e0:     	add	x29, sp, #16
1000042e4:     	sub	sp, sp, #752
1000042e8:     	str	x0, [sp, #296]
;     const int N = state.range(0);
1000042ec:     	ldr	x8, [sp, #296]
1000042f0:     	str	x8, [sp, #312]
1000042f4:     	str	xzr, [sp, #304]
1000042f8:     	ldr	x8, [sp, #312]
1000042fc:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
100004300:     	add	x0, x8, #32