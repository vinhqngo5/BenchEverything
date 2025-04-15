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
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001990:     	b.eq	0x100001b94 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x244>
100001994:     	cmp	w20, #0
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001998:     	b.le	0x100001b7c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x22c>
10000199c:     	str	x23, [sp]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
1000019a0:     	b	0x1000019b0 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x60>
1000019a4:     	subs	x22, x22, #1
1000019a8:     	ldr	x23, [sp]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
1000019ac:     	b.eq	0x100001b94 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x244>
1000019b0:     	mov	x0, x23
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
1000019dc:     	b	0x1000019f8 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0xa8>
1000019e0:     	str	w25, [x27], #4
1000019e4:     	str	x27, [sp, #40]
1000019e8:     	mov	x19, x27
1000019ec:     	add	w25, w25, #1
1000019f0:     	cmp	w25, w20
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
1000019f4:     	b.eq	0x100001b68 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x218>
1000019f8:     	cmp	x27, x23
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
1000019fc:     	b.ne	0x1000019e0 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x90>
100001a00:     	sub	x24, x27, x21
100001a04:     	asr	x23, x24, #2
100001a08:     	add	x8, x23, #1
100001a0c:     	lsr	x9, x8, #62
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a10:     	cbnz	x9, 0x100001d38 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3e8>
100001a14:     	asr	x9, x24, #1
100001a18:     	cmp	x9, x8
100001a1c:     	csel	x8, x9, x8, hi
100001a20:     	mov	x9, #9223372036854775804
100001a24:     	cmp	x24, x9
100001a28:     	mov	x9, #4611686018427387903
100001a2c:     	csel	x28, x8, x9, lo
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a30:     	cbz	x28, 0x100001a5c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x10c>
100001a34:     	lsr	x8, x28, #62
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a38:     	cbnz	x8, 0x100001d4c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3fc>
100001a3c:     	lsl	x0, x28, #2
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a54:     	b.ne	0x100001a74 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x124>
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a58:     	b	0x100001a98 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x148>
100001a5c:     	mov	x0, #0
100001a60:     	add	x26, x0, x23, lsl #2
100001a64:     	mov	x19, x26
100001a68:     	str	w25, [x19], #4
100001a6c:     	cmp	x27, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a70:     	b.eq	0x100001a98 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x148>
100001a74:     	sub	x9, x27, #4
100001a78:     	sub	x8, x9, x21
100001a7c:     	cmp	x8, #188
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a80:     	b.hs	0x100001ac4 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x174>
100001a84:     	mov	x8, x27
100001a88:     	ldr	w9, [x8, #-4]!
100001a8c:     	str	w9, [x26, #-4]!
100001a90:     	cmp	x8, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001a94:     	b.ne	0x100001a88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x138>
100001a98:     	add	x23, x0, x28, lsl #2
100001a9c:     	str	x19, [sp, #40]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001aa0:     	cbz	x21, 0x100001aac <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x15c>
100001aa4:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001abc:     	b.ne	0x1000019f8 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0xa8>
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001ac0:     	b	0x100001b68 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x218>
100001ac4:     	and	x10, x8, #0xfffffffffffffffc
100001ac8:     	add	x11, x0, x24
100001acc:     	sub	x11, x11, #4
100001ad0:     	sub	x12, x11, x10
100001ad4:     	cmp	x12, x11
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001ad8:     	b.hi	0x100001b0c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x1bc>
100001adc:     	sub	x10, x9, x10
100001ae0:     	cmp	x10, x9
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001ae4:     	b.hi	0x100001b04 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x1b4>
100001ae8:     	add	x10, x0, x24
100001aec:     	sub	x9, x9, x10
100001af0:     	add	x9, x9, #4
100001af4:     	cmp	x9, #64
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001af8:     	b.hs	0x100001b14 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x1c4>
100001afc:     	mov	x8, x27
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b00:     	b	0x100001a88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x138>
100001b04:     	mov	x8, x27
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b08:     	b	0x100001a88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x138>
100001b0c:     	mov	x8, x27
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b10:     	b	0x100001a88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x138>
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
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b58:     	cbnz	x13, 0x100001b3c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x1ec>
100001b5c:     	cmp	x9, x10
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b60:     	b.ne	0x100001a88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x138>
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b64:     	b	0x100001a98 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x148>
100001b68:     	str	x26, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b6c:     	cbz	x21, 0x1000019a4 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x54>
100001b70:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b78:     	b	0x1000019a4 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x54>
100001b7c:     	mov	x0, x23
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001b90:     	b.ne	0x100001b7c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x22c>
100001b94:     	mov	x0, x23
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001ba0:     	cbz	w8, 0x100001d5c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x40c>
100001ba4:     	ldp	x10, x8, [x23, #8]
100001ba8:     	ldr	x9, [x23]
100001bac:     	sub	x8, x8, x9
100001bb0:     	add	x22, x8, x10
100001bb4:     	add	x21, x23, #64
100001bb8:     	mov	w8, #16
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001bbc:     	adrp	x9, 0x100031000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x32c>
100001bc0:     	add	x9, x9, #4025
100001bc4:     	strb	w8, [sp, #55]
100001bc8:     	ldr	q0, [x9]
100001bcc:     	str	q0, [sp, #32]
100001bd0:     	strb	wzr, [sp, #48]
100001bd4:     	add	x8, sp, #32
100001bd8:     	str	x8, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001bdc:     	adrp	x2, 0x100034000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x358>
100001be0:     	ldr	x2, [x2, #440]
100001be4:     	add	x1, sp, #32
100001be8:     	add	x3, sp, #8
100001bec:     	add	x4, sp, #56
100001bf0:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c0c:     	adrp	x8, 0x10002f000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x374>
100001c10:     	ldr	d0, [x8, #176]
100001c14:     	str	d0, [x0, #64]
100001c18:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c1c:     	tbz	w8, #31, 0x100001c28 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x2d8>
100001c20:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c2c:     	cbz	w8, 0x100001d64 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x414>
100001c30:     	ldp	x10, x8, [x23, #8]
100001c34:     	ldr	x9, [x23]
100001c38:     	sub	x8, x8, x9
100001c3c:     	add	x22, x8, x10
100001c40:     	mov	w8, #16
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c44:     	adrp	x9, 0x100031000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3b4>
100001c48:     	add	x9, x9, #4042
100001c4c:     	strb	w8, [sp, #55]
100001c50:     	ldr	q0, [x9]
100001c54:     	str	q0, [sp, #32]
100001c58:     	strb	wzr, [sp, #48]
100001c5c:     	add	x8, sp, #32
100001c60:     	str	x8, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c64:     	adrp	x2, 0x100034000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3e0>
100001c68:     	ldr	x2, [x2, #440]
100001c6c:     	add	x1, sp, #32
100001c70:     	add	x3, sp, #8
100001c74:     	add	x4, sp, #56
100001c78:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c8c:     	adrp	x8, 0x10002f000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3f4>
100001c90:     	ldr	d1, [x8, #184]
100001c94:     	stp	d0, d1, [x0, #56]
100001c98:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001c9c:     	tbz	w8, #31, 0x100001ca8 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x358>
100001ca0:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001cb4:     	adrp	x1, 0x100031000 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x424>
100001cb8:     	add	x1, x1, #4008
100001cbc:     	add	x0, sp, #8
100001cc0:     	mov	w2, #9
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001cf0:     	tbnz	w8, #31, 0x100001d1c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3cc>
100001cf4:     	ldrsb	w8, [sp, #31]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001cf8:     	tbnz	w8, #31, 0x100001d2c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3dc>
100001cfc:     	ldp	x29, x30, [sp, #144]
100001d00:     	ldp	x20, x19, [sp, #128]
100001d04:     	ldp	x22, x21, [sp, #112]
100001d08:     	ldp	x24, x23, [sp, #96]
100001d0c:     	ldp	x26, x25, [sp, #80]
100001d10:     	ldp	x28, x27, [sp, #64]
100001d14:     	add	sp, sp, #160
100001d18:     	ret
100001d1c:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d28:     	tbz	w8, #31, 0x100001cfc <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3ac>
100001d2c:     	ldr	x0, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d34:     	b	0x100001cfc <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x3ac>
100001d38:     	str	x26, [sp, #32]
100001d3c:     	str	x27, [sp, #48]
100001d40:     	add	x0, sp, #32
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d48:     	b	0x100001d58 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x408>
100001d4c:     	str	x26, [sp, #32]
100001d50:     	str	x27, [sp, #48]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d60:     	b	0x100001bb4 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x264>
100001d64:     	mov	x22, #0
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d68:     	b	0x100001c40 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x2f0>
100001d6c:     	mov	x19, x0
100001d70:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d74:     	tbz	w8, #31, 0x100001d88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x438>
100001d78:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d80:     	b	0x100001d88 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x438>
100001d84:     	mov	x19, x0
100001d88:     	ldrsb	w8, [sp, #31]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d8c:     	tbz	w8, #31, 0x100001de0 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x490>
100001d90:     	ldr	x0, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d94:     	b	0x100001ddc <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x48c>
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001d98:     	b	0x100001d9c <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x44c>
100001d9c:     	mov	x19, x0
100001da0:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001da4:     	tbz	w8, #31, 0x100001de0 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x490>
100001da8:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001dac:     	b	0x100001ddc <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x48c>
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001dc4:     	b	0x100001dd0 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x480>
100001dc8:     	mov	x19, x0
100001dcc:     	ldr	x21, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>>
100001dd0:     	cbz	x21, 0x100001de0 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)+0x490>
100001dd4:     	str	x21, [sp, #40]
100001dd8:     	mov	x0, x21