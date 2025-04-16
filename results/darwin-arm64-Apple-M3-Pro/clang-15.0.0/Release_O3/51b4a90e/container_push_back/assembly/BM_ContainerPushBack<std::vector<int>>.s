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
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
0000000100001950 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)>:
100001950:     	sub	sp, sp, #160
100001954:     	stp	x28, x27, [sp, #64]
100001958:     	stp	x26, x25, [sp, #80]
10000195c:     	stp	x24, x23, [sp, #96]
100001960:     	stp	x22, x21, [sp, #112]
100001964:     	stp	x20, x19, [sp, #128]
100001968:     	stp	x29, x30, [sp, #144]
10000196c:     	add	x29, sp, #144
100001970:     	mov	x23, x0
100001974:     	ldr	x8, [x0, #32]
100001978:     	ldr	x20, [x8]
10000197c:     	ldr	w19, [x0, #28]
100001980:     	ldr	x22, [x0, #16]
100001984:     	bl	0x1000040dc <benchmark::State::StartKeepRunning()>
100001988:     	cmp	w19, #0
10000198c:     	ccmp	x22, #0, #4, eq
100001994:     	cmp	w20, #0
10000199c:     	str	x23, [sp]
1000019a4:     	subs	x22, x22, #1
1000019a8:     	ldr	x23, [sp]
1000019b0:     	mov	x0, x23
1000019b4:     	bl	0x1000038fc <benchmark::State::PauseTiming()>
1000019b8:     	stp	xzr, xzr, [sp, #32]
1000019bc:     	str	xzr, [sp, #48]
1000019c0:     	mov	x0, x23
1000019c4:     	bl	0x100003e10 <benchmark::State::ResumeTiming()>
1000019c8:     	mov	x21, #0
1000019cc:     	mov	x27, #0
1000019d0:     	mov	x23, #0
1000019d4:     	mov	w25, #0
1000019d8:     	ldr	x26, [sp, #32]
1000019e0:     	str	w25, [x27], #4
1000019e4:     	str	x27, [sp, #40]
1000019e8:     	mov	x19, x27
1000019ec:     	add	w25, w25, #1
1000019f0:     	cmp	w25, w20
1000019f8:     	cmp	x27, x23
100001a00:     	sub	x24, x27, x21
100001a04:     	asr	x23, x24, #2
100001a08:     	add	x8, x23, #1
100001a0c:     	lsr	x9, x8, #62
100001a14:     	asr	x9, x24, #1
100001a18:     	cmp	x9, x8
100001a1c:     	csel	x8, x9, x8, hi
100001a20:     	mov	x9, #9223372036854775804
100001a24:     	cmp	x24, x9
100001a28:     	mov	x9, #4611686018427387903
100001a2c:     	csel	x28, x8, x9, lo
100001a34:     	lsr	x8, x28, #62
100001a3c:     	lsl	x0, x28, #2
100001a40:     	bl	0x10002edec <_vsnprintf+0x10002edec>
100001a44:     	add	x26, x0, x23, lsl #2
100001a48:     	mov	x19, x26
100001a4c:     	str	w25, [x19], #4
100001a50:     	cmp	x27, x21
100001a5c:     	mov	x0, #0
100001a60:     	add	x26, x0, x23, lsl #2
100001a64:     	mov	x19, x26
100001a68:     	str	w25, [x19], #4
100001a6c:     	cmp	x27, x21
100001a74:     	sub	x9, x27, #4
100001a78:     	sub	x8, x9, x21
100001a7c:     	cmp	x8, #188
100001a84:     	mov	x8, x27
100001a88:     	ldr	w9, [x8, #-4]!
100001a8c:     	str	w9, [x26, #-4]!
100001a90:     	cmp	x8, x21
100001a98:     	add	x23, x0, x28, lsl #2
100001a9c:     	str	x19, [sp, #40]
100001aa4:     	mov	x0, x21
100001aa8:     	bl	0x10002edd4 <_vsnprintf+0x10002edd4>
100001aac:     	mov	x21, x26
100001ab0:     	add	w25, w25, #1
100001ab4:     	mov	x27, x19
100001ab8:     	cmp	w25, w20
100001ac4:     	and	x10, x8, #0xfffffffffffffffc
100001ac8:     	add	x11, x0, x24
100001acc:     	sub	x11, x11, #4
100001ad0:     	sub	x12, x11, x10
100001ad4:     	cmp	x12, x11
100001adc:     	sub	x10, x9, x10
100001ae0:     	cmp	x10, x9
100001ae8:     	add	x10, x0, x24
100001aec:     	sub	x9, x9, x10
100001af0:     	add	x9, x9, #4
100001af4:     	cmp	x9, #64
100001afc:     	mov	x8, x27
100001b04:     	mov	x8, x27
100001b0c:     	mov	x8, x27
100001b14:     	lsr	x8, x8, #2
100001b18:     	add	x9, x8, #1
100001b1c:     	and	x10, x9, #0x7ffffffffffffff0
100001b20:     	lsl	x11, x10, #2
100001b24:     	sub	x8, x27, x11
100001b28:     	sub	x26, x26, x11
100001b2c:     	sub	x11, x27, #32
100001b30:     	add	x12, x0, x23, lsl #2
100001b34:     	sub	x12, x12, #32
100001b38:     	mov	x13, x10
100001b3c:     	ldp	q1, q0, [x11]
100001b40:     	ldp	q3, q2, [x11, #-32]
100001b44:     	stp	q1, q0, [x12]
100001b48:     	stp	q3, q2, [x12, #-32]
100001b4c:     	sub	x11, x11, #64
100001b50:     	sub	x12, x12, #64
100001b54:     	sub	x13, x13, #16
100001b5c:     	cmp	x9, x10
100001b68:     	str	x26, [sp, #32]
100001b70:     	mov	x0, x21
100001b74:     	bl	0x10002edd4 <_vsnprintf+0x10002edd4>
100001b7c:     	mov	x0, x23
100001b80:     	bl	0x1000038fc <benchmark::State::PauseTiming()>
100001b84:     	mov	x0, x23
100001b88:     	bl	0x100003e10 <benchmark::State::ResumeTiming()>
100001b8c:     	subs	x22, x22, #1
100001b94:     	mov	x0, x23
100001b98:     	bl	0x100004188 <benchmark::State::FinishKeepRunning()>
100001b9c:     	ldrb	w8, [x23, #24]
100001ba4:     	ldp	x10, x8, [x23, #8]
100001ba8:     	ldr	x9, [x23]
100001bac:     	sub	x8, x8, x9
100001bb0:     	add	x22, x8, x10
100001bb4:     	add	x21, x23, #64
100001bb8:     	mov	w8, #16
100001bc0:     	add	x9, x9, #4025
100001bc4:     	strb	w8, [sp, #55]
100001bc8:     	ldr	q0, [x9]
100001bcc:     	str	q0, [sp, #32]
100001bd0:     	strb	wzr, [sp, #48]
100001bd4:     	add	x8, sp, #32
100001bd8:     	str	x8, [sp, #8]
100001be0:     	ldr	x2, [x2, #440]
100001be4:     	add	x1, sp, #32
100001be8:     	add	x3, sp, #8
100001bec:     	add	x4, sp, #56
100001bf0:     	mov	x0, x21