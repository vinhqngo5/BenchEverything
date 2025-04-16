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
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
000000010000218c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
10000218c:     	sub	sp, sp, #144
100002190:     	stp	x26, x25, [sp, #64]
100002194:     	stp	x24, x23, [sp, #80]
100002198:     	stp	x22, x21, [sp, #96]
10000219c:     	stp	x20, x19, [sp, #112]
1000021a0:     	stp	x29, x30, [sp, #128]
1000021a4:     	add	x29, sp, #128
1000021a8:     	mov	x19, x0
1000021ac:     	ldr	x8, [x0, #32]
1000021b0:     	ldr	x20, [x8]
1000021b4:     	ldr	w22, [x0, #28]
1000021b8:     	ldr	x21, [x0, #16]
1000021bc:     	bl	0x1000040dc <benchmark::State::StartKeepRunning()>
1000021c0:     	cmp	w22, #0
1000021c4:     	ccmp	x21, #0, #4, eq
1000021cc:     	add	x22, sp, #32
1000021d0:     	cmp	w20, #0
1000021dc:     	subs	x21, x21, #1
1000021e4:     	mov	x0, x19
1000021e8:     	bl	0x1000038fc <benchmark::State::PauseTiming()>
1000021ec:     	stp	x22, x22, [sp, #32]
1000021f0:     	str	xzr, [sp, #48]
1000021f4:     	mov	x0, x19
1000021f8:     	bl	0x100003e10 <benchmark::State::ResumeTiming()>
1000021fc:     	mov	x23, #0
100002200:     	ldr	x25, [sp, #32]
100002204:     	ldr	x24, [sp, #48]
100002208:     	mov	w0, #24
10000220c:     	bl	0x10002edec <_vsnprintf+0x10002edec>
100002210:     	mov	x8, x0
100002214:     	str	w23, [x0, #16]
100002218:     	stp	x25, x22, [x0]
10000221c:     	str	x0, [x25, #8]
100002220:     	add	x9, x24, x23
100002224:     	add	x9, x9, #1
100002228:     	str	x0, [sp, #32]
10000222c:     	str	x9, [sp, #48]
100002230:     	add	x23, x23, #1
100002234:     	mov	x25, x0
100002238:     	cmp	w20, w23
100002240:     	add	x9, x24, x23
100002248:     	ldr	x0, [sp, #40]
10000224c:     	ldr	x9, [x8, #8]
100002250:     	ldr	x10, [x0]
100002254:     	str	x9, [x10, #8]
100002258:     	ldr	x8, [x8, #8]
10000225c:     	str	x10, [x8]
100002260:     	str	xzr, [sp, #48]
100002264:     	cmp	x0, x22
10000226c:     	ldr	x23, [x0, #8]
100002270:     	bl	0x10002edd4 <_vsnprintf+0x10002edd4>
100002274:     	mov	x0, x23
100002278:     	cmp	x23, x22
100002284:     	subs	x21, x21, #1
10000228c:     	mov	x0, x19
100002290:     	bl	0x1000038fc <benchmark::State::PauseTiming()>
100002294:     	stp	x22, x22, [sp, #32]
100002298:     	str	xzr, [sp, #48]
10000229c:     	mov	x0, x19
1000022a0:     	bl	0x100003e10 <benchmark::State::ResumeTiming()>
1000022a4:     	ldr	x8, [sp, #48]
1000022ac:     	ldp	x8, x0, [sp, #32]
1000022b0:     	ldr	x9, [x8, #8]
1000022b4:     	ldr	x10, [x0]
1000022b8:     	str	x9, [x10, #8]
1000022bc:     	ldr	x8, [x8, #8]
1000022c0:     	str	x10, [x8]
1000022c4:     	str	xzr, [sp, #48]
1000022c8:     	cmp	x0, x22
1000022d0:     	ldr	x23, [x0, #8]
1000022d4:     	bl	0x10002edd4 <_vsnprintf+0x10002edd4>
1000022d8:     	mov	x0, x23
1000022dc:     	cmp	x23, x22
1000022e8:     	mov	x0, x19
1000022ec:     	bl	0x100004188 <benchmark::State::FinishKeepRunning()>
1000022f0:     	ldrb	w8, [x19, #24]
1000022f8:     	ldp	x10, x8, [x19, #8]
1000022fc:     	ldr	x9, [x19]
100002300:     	sub	x8, x8, x9
100002304:     	add	x23, x8, x10
100002308:     	add	x21, x19, #64
10000230c:     	mov	w8, #16
100002314:     	add	x9, x9, #4025
100002318:     	strb	w8, [sp, #55]
10000231c:     	ldr	q0, [x9]
100002320:     	str	q0, [sp, #32]
100002324:     	strb	wzr, [sp, #48]
100002328:     	add	x8, sp, #32
10000232c:     	str	x8, [sp, #8]
100002334:     	ldr	x2, [x2, #440]
100002338:     	add	x1, sp, #32
10000233c:     	add	x3, sp, #8
100002340:     	add	x4, sp, #56
100002344:     	mov	x0, x21