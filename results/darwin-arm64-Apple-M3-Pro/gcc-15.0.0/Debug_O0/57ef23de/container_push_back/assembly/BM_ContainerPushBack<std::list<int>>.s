// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>> (matched on 'BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>')
00000001000042f4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
1000042f4:     	stp	x28, x27, [sp, #-32]!
1000042f8:     	stp	x29, x30, [sp, #16]
1000042fc:     	add	x29, sp, #16
100004300:     	sub	sp, sp, #752
100004304:     	str	x0, [sp, #296]
;     const int N = state.range(0);
100004308:     	ldr	x8, [sp, #296]
10000430c:     	str	x8, [sp, #312]
100004310:     	str	xzr, [sp, #304]
100004314:     	ldr	x8, [sp, #312]
100004318:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
10000431c:     	add	x0, x8, #32