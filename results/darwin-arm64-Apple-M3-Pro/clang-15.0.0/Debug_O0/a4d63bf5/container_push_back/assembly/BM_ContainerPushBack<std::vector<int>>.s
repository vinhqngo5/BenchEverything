// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>> (matched on 'BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>')
000000010000372c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
10000372c:     	stp	x28, x27, [sp, #-32]!
100003730:     	stp	x29, x30, [sp, #16]
100003734:     	add	x29, sp, #16
100003738:     	sub	sp, sp, #752
10000373c:     	str	x0, [sp, #296]
;     const int N = state.range(0);
100003740:     	ldr	x8, [sp, #296]
100003744:     	str	x8, [sp, #312]
100003748:     	str	xzr, [sp, #304]
10000374c:     	ldr	x8, [sp, #312]
100003750:     	str	x8, [sp, #144]
;     assert(range_.size() > pos);
100003754:     	add	x0, x8, #32