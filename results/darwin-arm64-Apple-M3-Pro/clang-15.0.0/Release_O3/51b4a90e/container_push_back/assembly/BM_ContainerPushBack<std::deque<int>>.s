// Template definition for BM_ContainerPushBack:
/*
template <typename Container>
static void BM_ContainerPushBack(benchmark::State& state) {
    const int N = state.range(0);

    for (auto _ : state) {
        state.PauseTiming();
        Container c;
        state.ResumeTiming();

        for (int i = 0; i < N; ++i) {
            c.push_back(i);
        }
    }

    state.SetItemsProcessed(int64_t(state.iterations()) * N);
    state.SetBytesProcessed(int64_t(state.iterations()) * N * sizeof(int));
    state.SetLabel(std::to_string(N) + " elements");
}
*/

// Assembly:
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
0000000100001de8 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
100001de8:     	sub	sp, sp, #160
100001dec:     	stp	x24, x23, [sp, #96]
100001df0:     	stp	x22, x21, [sp, #112]
100001df4:     	stp	x20, x19, [sp, #128]
100001df8:     	stp	x29, x30, [sp, #144]
100001dfc:     	add	x29, sp, #144
100001e00:     	mov	x19, x0
100001e04:     	ldr	x8, [x0, #32]
100001e08:     	ldr	x20, [x8]
100001e0c:     	ldr	w22, [x0, #28]
100001e10:     	ldr	x21, [x0, #16]
100001e14:     	bl	0x1000040dc <benchmark::State::StartKeepRunning()>
100001e18:     	cmp	w22, #0
100001e1c:     	ccmp	x21, #0, #4, eq
100001e24:     	mov	x0, x19
100001e28:     	bl	0x100004188 <benchmark::State::FinishKeepRunning()>
100001e2c:     	ldrb	w8, [x19, #24]
100001e34:     	ldp	x10, x8, [x19, #8]
100001e38:     	ldr	x9, [x19]
100001e3c:     	sub	x8, x8, x9
100001e40:     	add	x23, x8, x10
100001e44:     	add	x21, x19, #64
100001e48:     	mov	w8, #16
100001e50:     	add	x9, x9, #4025
100001e54:     	strb	w8, [sp, #55]
100001e58:     	ldr	q0, [x9]
100001e5c:     	str	q0, [sp, #32]
100001e60:     	strb	wzr, [sp, #48]
100001e64:     	add	x8, sp, #32
100001e68:     	str	x8, [sp, #8]
100001e70:     	ldr	x2, [x2, #440]
100001e74:     	add	x1, sp, #32
100001e78:     	add	x3, sp, #8
100001e7c:     	sub	x4, x29, #56
100001e80:     	mov	x0, x21