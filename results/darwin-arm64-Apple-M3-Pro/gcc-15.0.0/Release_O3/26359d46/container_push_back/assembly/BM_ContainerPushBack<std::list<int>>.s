// Template definition for BM_ContainerPushBack:
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
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000021c8:     	b.eq	0x1000022e8 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x15c>
1000021cc:     	add	x22, sp, #32
1000021d0:     	cmp	w20, #0
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000021d4:     	b.gt	0x1000021e4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x58>
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000021d8:     	b	0x10000228c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x100>
1000021dc:     	subs	x21, x21, #1
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000021e0:     	b.eq	0x1000022e8 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x15c>
1000021e4:     	mov	x0, x19
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
10000223c:     	b.ne	0x100002208 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x7c>
100002240:     	add	x9, x24, x23
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002244:     	cbz	x9, 0x1000021dc <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x50>
100002248:     	ldr	x0, [sp, #40]
10000224c:     	ldr	x9, [x8, #8]
100002250:     	ldr	x10, [x0]
100002254:     	str	x9, [x10, #8]
100002258:     	ldr	x8, [x8, #8]
10000225c:     	str	x10, [x8]
100002260:     	str	xzr, [sp, #48]
100002264:     	cmp	x0, x22
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002268:     	b.eq	0x1000021dc <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x50>
10000226c:     	ldr	x23, [x0, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
10000227c:     	b.ne	0x10000226c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0xe0>
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002280:     	b	0x1000021dc <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x50>
100002284:     	subs	x21, x21, #1
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002288:     	b.eq	0x1000022e8 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x15c>
10000228c:     	mov	x0, x19
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000022a8:     	cbz	x8, 0x100002284 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0xf8>
1000022ac:     	ldp	x8, x0, [sp, #32]
1000022b0:     	ldr	x9, [x8, #8]
1000022b4:     	ldr	x10, [x0]
1000022b8:     	str	x9, [x10, #8]
1000022bc:     	ldr	x8, [x8, #8]
1000022c0:     	str	x10, [x8]
1000022c4:     	str	xzr, [sp, #48]
1000022c8:     	cmp	x0, x22
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000022cc:     	b.eq	0x100002284 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0xf8>
1000022d0:     	ldr	x23, [x0, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000022e0:     	b.ne	0x1000022d0 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x144>
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000022e4:     	b	0x100002284 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0xf8>
1000022e8:     	mov	x0, x19
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000022f4:     	cbz	w8, 0x100002488 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2fc>
1000022f8:     	ldp	x10, x8, [x19, #8]
1000022fc:     	ldr	x9, [x19]
100002300:     	sub	x8, x8, x9
100002304:     	add	x23, x8, x10
100002308:     	add	x21, x19, #64
10000230c:     	mov	w8, #16
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002310:     	adrp	x9, 0x100031000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x240>
100002314:     	add	x9, x9, #4025
100002318:     	strb	w8, [sp, #55]
10000231c:     	ldr	q0, [x9]
100002320:     	str	q0, [sp, #32]
100002324:     	strb	wzr, [sp, #48]
100002328:     	add	x8, sp, #32
10000232c:     	str	x8, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002330:     	adrp	x2, 0x100034000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x26c>
100002334:     	ldr	x2, [x2, #440]
100002338:     	add	x1, sp, #32
10000233c:     	add	x3, sp, #8
100002340:     	add	x4, sp, #56
100002344:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002360:     	adrp	x8, 0x10002f000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x288>
100002364:     	ldr	d0, [x8, #176]
100002368:     	str	d0, [x0, #64]
10000236c:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002370:     	tbz	w8, #31, 0x10000237c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x1f0>
100002374:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002380:     	cbz	w8, 0x100002490 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x304>
100002384:     	ldp	x10, x8, [x19, #8]
100002388:     	ldr	x9, [x19]
10000238c:     	sub	x8, x8, x9
100002390:     	add	x23, x8, x10
100002394:     	mov	w8, #16
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002398:     	adrp	x9, 0x100031000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2c8>
10000239c:     	add	x9, x9, #4042
1000023a0:     	strb	w8, [sp, #55]
1000023a4:     	ldr	q0, [x9]
1000023a8:     	str	q0, [sp, #32]
1000023ac:     	strb	wzr, [sp, #48]
1000023b0:     	add	x8, sp, #32
1000023b4:     	str	x8, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000023b8:     	adrp	x2, 0x100034000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2f4>
1000023bc:     	ldr	x2, [x2, #440]
1000023c0:     	add	x1, sp, #32
1000023c4:     	add	x3, sp, #8
1000023c8:     	add	x4, sp, #56
1000023cc:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000023e0:     	adrp	x8, 0x10002f000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x308>
1000023e4:     	ldr	d1, [x8, #184]
1000023e8:     	stp	d0, d1, [x0, #56]
1000023ec:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000023f0:     	tbz	w8, #31, 0x1000023fc <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x270>
1000023f4:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002408:     	adrp	x1, 0x100031000 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x338>
10000240c:     	add	x1, x1, #4008
100002410:     	add	x0, sp, #8
100002414:     	mov	w2, #9
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002444:     	tbnz	w8, #31, 0x10000246c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2e0>
100002448:     	ldrsb	w8, [sp, #31]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
10000244c:     	tbnz	w8, #31, 0x10000247c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2f0>
100002450:     	ldp	x29, x30, [sp, #128]
100002454:     	ldp	x20, x19, [sp, #112]
100002458:     	ldp	x22, x21, [sp, #96]
10000245c:     	ldp	x24, x23, [sp, #80]
100002460:     	ldp	x26, x25, [sp, #64]
100002464:     	add	sp, sp, #144
100002468:     	ret
10000246c:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002478:     	tbz	w8, #31, 0x100002450 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2c4>
10000247c:     	ldr	x0, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002484:     	b	0x100002450 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x2c4>
100002488:     	mov	x23, #0
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
10000248c:     	b	0x100002308 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x17c>
100002490:     	mov	x23, #0
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
100002494:     	b	0x100002394 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x208>
100002498:     	mov	x19, x0
10000249c:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024a0:     	tbz	w8, #31, 0x1000024b4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x328>
1000024a4:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024ac:     	b	0x1000024b4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x328>
1000024b0:     	mov	x19, x0
1000024b4:     	ldrsb	w8, [sp, #31]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024b8:     	tbz	w8, #31, 0x100002500 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x374>
1000024bc:     	ldr	x0, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024cc:     	b	0x1000024d0 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x344>
1000024d0:     	mov	x19, x0
1000024d4:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024d8:     	tbz	w8, #31, 0x100002500 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x374>
1000024dc:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024ec:     	b	0x1000024f4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x368>
// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>>
1000024f0:     	b	0x1000024f4 <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)+0x368>
1000024f4:     	mov	x19, x0
1000024f8:     	add	x0, sp, #32