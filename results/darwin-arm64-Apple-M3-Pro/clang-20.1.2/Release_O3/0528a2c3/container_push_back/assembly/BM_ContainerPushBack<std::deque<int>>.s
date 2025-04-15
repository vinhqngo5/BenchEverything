// Source code for BM_ContainerPushBack<std::deque<int>> (manually added):
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
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001e20:     	b.ne	0x100001fac <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1c4>
100001e24:     	mov	x0, x19
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001e30:     	cbz	w8, 0x100002110 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x328>
100001e34:     	ldp	x10, x8, [x19, #8]
100001e38:     	ldr	x9, [x19]
100001e3c:     	sub	x8, x8, x9
100001e40:     	add	x23, x8, x10
100001e44:     	add	x21, x19, #64
100001e48:     	mov	w8, #16
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001e4c:     	adrp	x9, 0x100031000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x124>
100001e50:     	add	x9, x9, #4025
100001e54:     	strb	w8, [sp, #55]
100001e58:     	ldr	q0, [x9]
100001e5c:     	str	q0, [sp, #32]
100001e60:     	strb	wzr, [sp, #48]
100001e64:     	add	x8, sp, #32
100001e68:     	str	x8, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001e6c:     	adrp	x2, 0x100034000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x150>
100001e70:     	ldr	x2, [x2, #440]
100001e74:     	add	x1, sp, #32
100001e78:     	add	x3, sp, #8
100001e7c:     	sub	x4, x29, #56
100001e80:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001e9c:     	adrp	x8, 0x10002f000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x16c>
100001ea0:     	ldr	d0, [x8, #176]
100001ea4:     	str	d0, [x0, #64]
100001ea8:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001eac:     	tbz	w8, #31, 0x100001eb8 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0xd0>
100001eb0:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001ebc:     	cbz	w8, 0x100002118 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x330>
100001ec0:     	ldp	x10, x8, [x19, #8]
100001ec4:     	ldr	x9, [x19]
100001ec8:     	sub	x8, x8, x9
100001ecc:     	add	x23, x8, x10
100001ed0:     	mov	w8, #16
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001ed4:     	adrp	x9, 0x100031000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1ac>
100001ed8:     	add	x9, x9, #4042
100001edc:     	strb	w8, [sp, #55]
100001ee0:     	ldr	q0, [x9]
100001ee4:     	str	q0, [sp, #32]
100001ee8:     	strb	wzr, [sp, #48]
100001eec:     	add	x8, sp, #32
100001ef0:     	str	x8, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001ef4:     	adrp	x2, 0x100034000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1d8>
100001ef8:     	ldr	x2, [x2, #440]
100001efc:     	add	x1, sp, #32
100001f00:     	add	x3, sp, #8
100001f04:     	sub	x4, x29, #56
100001f08:     	mov	x0, x21
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001f1c:     	adrp	x8, 0x10002f000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1ec>
100001f20:     	ldr	d1, [x8, #184]
100001f24:     	stp	d0, d1, [x0, #56]
100001f28:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001f2c:     	tbz	w8, #31, 0x100001f38 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x150>
100001f30:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001f44:     	adrp	x1, 0x100031000 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x21c>
100001f48:     	add	x1, x1, #4008
100001f4c:     	add	x0, sp, #8
100001f50:     	mov	w2, #9
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001f80:     	tbnz	w8, #31, 0x1000020e0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2f8>
100001f84:     	ldrsb	w8, [sp, #31]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001f88:     	tbnz	w8, #31, 0x1000020f0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x308>
100001f8c:     	ldp	x29, x30, [sp, #144]
100001f90:     	ldp	x20, x19, [sp, #128]
100001f94:     	ldp	x22, x21, [sp, #112]
100001f98:     	ldp	x24, x23, [sp, #96]
100001f9c:     	add	sp, sp, #160
100001fa0:     	ret
100001fa4:     	subs	x21, x21, #1
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001fa8:     	b.eq	0x100001e24 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x3c>
100001fac:     	mov	x0, x19
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001fcc:     	b.le	0x100002040 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x258>
100001fd0:     	mov	w24, #0
100001fd4:     	ldp	x22, x23, [sp, #40]
100001fd8:     	ldp	x8, x9, [sp, #64]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100001fdc:     	b	0x100002008 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x220>
100001fe0:     	lsr	x11, x10, #7
100001fe4:     	and	x11, x11, #0x1fffffffffffff8
100001fe8:     	ldr	x11, [x22, x11]
100001fec:     	and	x10, x10, #0x3ff
100001ff0:     	str	w24, [x11, x10, lsl #2]
100001ff4:     	add	x9, x9, #1
100001ff8:     	str	x9, [sp, #72]
100001ffc:     	add	w24, w24, #1
100002000:     	cmp	w20, w24
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002004:     	b.eq	0x100002044 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x25c>
100002008:     	subs	x10, x23, x22
10000200c:     	lsl	x10, x10, #7
100002010:     	sub	x10, x10, #1
100002014:     	cmp	x23, x22
100002018:     	csel	x11, xzr, x10, eq
10000201c:     	add	x10, x9, x8
100002020:     	cmp	x11, x10
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002024:     	b.ne	0x100001fe0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1f8>
100002028:     	add	x0, sp, #32
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
10000203c:     	b	0x100001fe0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1f8>
100002040:     	ldp	x22, x23, [sp, #40]
100002044:     	str	xzr, [sp, #72]
100002048:     	sub	x8, x23, x22
10000204c:     	cmp	x8, #17
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002050:     	b.lo	0x100002074 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x28c>
100002054:     	ldr	x0, [x22]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002070:     	b.hi	0x100002054 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x26c>
100002074:     	lsr	x8, x8, #3
100002078:     	cmp	x8, #1
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
10000207c:     	b.eq	0x100002090 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2a8>
100002080:     	cmp	x8, #2
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002084:     	b.ne	0x100002098 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2b0>
100002088:     	mov	w8, #1024
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
10000208c:     	b	0x100002094 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2ac>
100002090:     	mov	w8, #512
100002094:     	str	x8, [sp, #64]
100002098:     	cmp	x22, x23
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
10000209c:     	b.eq	0x1000020d0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2e8>
1000020a0:     	ldr	x0, [x22], #8
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
1000020ac:     	b.ne	0x1000020a0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2b8>
1000020b0:     	ldp	x9, x8, [sp, #40]
1000020b4:     	cmp	x8, x9
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
1000020b8:     	b.eq	0x1000020d0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x2e8>
1000020bc:     	sub	x9, x9, x8
1000020c0:     	add	x9, x9, #7
1000020c4:     	and	x9, x9, #0xfffffffffffffff8
1000020c8:     	add	x8, x8, x9
1000020cc:     	str	x8, [sp, #48]
1000020d0:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
1000020d4:     	cbz	x0, 0x100001fa4 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1bc>
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
1000020dc:     	b	0x100001fa4 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1bc>
1000020e0:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
1000020ec:     	tbz	w8, #31, 0x100001f8c <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x1a4>
1000020f0:     	ldr	x0, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002114:     	b	0x100001e44 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x5c>
100002118:     	mov	x23, #0
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
10000211c:     	b	0x100001ed0 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0xe8>
100002120:     	mov	x19, x0
100002124:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002128:     	tbz	w8, #31, 0x10000213c <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x354>
10000212c:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002134:     	b	0x10000213c <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x354>
100002138:     	mov	x19, x0
10000213c:     	ldrsb	w8, [sp, #31]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002140:     	tbz	w8, #31, 0x100002184 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x39c>
100002144:     	ldr	x0, [sp, #8]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002154:     	b	0x100002158 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x370>
100002158:     	mov	x19, x0
10000215c:     	ldrsb	w8, [sp, #55]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002160:     	tbz	w8, #31, 0x100002184 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x39c>
100002164:     	ldr	x0, [sp, #32]
// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>>
100002174:     	b	0x100002178 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)+0x390>
100002178:     	mov	x19, x0
10000217c:     	add	x0, sp, #32