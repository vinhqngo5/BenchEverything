# Container Push Back Performance Benchmark

This benchmark compares the performance of `push_back` operations for different C++ containers:
- `std::vector<int>`
- `std::deque<int>`
- `std::list<int>`

The benchmark measures how performance scales across different container sizes, from 1,024 to 262,144 elements.

## Environment

| Property | Value |
|----------|-------|
| Timestamp | 2025-04-15T21:05:08.463523 |
| Platform ID | darwin-arm64-Apple-M3-Pro |
| CPU Model | Apple-M3-Pro |
| Compiler | gcc |
| Compiler Version | 15.0.0 |
| Build Flags | Release_O3 |
| Metadata Hash | 26359d46 |
| Metadata Source | build_flags_id=Release_O3:compiler_name=gcc:compiler_version=15.0.0:cpu=Apple-M3-Pro:machine=arm64:system=darwin |
| C++ Flags | -std=c++20 |
| CMake Build Type | Release |


## Benchmark Results

### Raw Performance Data

| Benchmark | Time (ns) | CPU (ns) | Iterations | Repetitions | Threads | Bytes/Second | Items/Second | 
| --------- | --------- | -------- | ---------- | ----------- | ------- | ------------ | ------------ | 
| BM_ContainerPushBack<std::vector<int>>/1024 | 1.49 | 1.37 | 534931 | 1 | 1 | 2986807767.33 | 746701941.83 | 
| BM_ContainerPushBack<std::vector<int>>/4096 | 2.51 | 2.46 | 270261 | 1 | 1 | 6668930165.31 | 1667232541.33 | 
| BM_ContainerPushBack<std::vector<int>>/32768 | 12.59 | 12.59 | 53419 | 1 | 1 | 10407911572.51 | 2601977893.13 | 
| BM_ContainerPushBack<std::vector<int>>/262144 | 160.99 | 160.59 | 4126 | 1 | 1 | 6529565154.92 | 1632391288.73 | 
| BM_ContainerPushBack<std::vector<int>>_BigO | N/A | N/A | N/A | 1 | 1 | N/A | N/A | 
| BM_ContainerPushBack<std::vector<int>>_RMS | N/A | N/A | N/A | 1 | 1 | N/A | N/A | 
| BM_ContainerPushBack<std::deque<int>>/1024 | 1.21 | 1.21 | 551185 | 1 | 1 | 3376238819.54 | 844059704.88 | 
| BM_ContainerPushBack<std::deque<int>>/4096 | 3.35 | 3.35 | 208539 | 1 | 1 | 4886526025.84 | 1221631506.46 | 
| BM_ContainerPushBack<std::deque<int>>/32768 | 22.26 | 22.12 | 31773 | 1 | 1 | 5926785494.10 | 1481696373.53 | 
| BM_ContainerPushBack<std::deque<int>>/262144 | 171.90 | 170.82 | 4048 | 1 | 1 | 6138603558.24 | 1534650889.56 | 
| BM_ContainerPushBack<std::deque<int>>_BigO | N/A | N/A | N/A | 1 | 1 | N/A | N/A | 
| BM_ContainerPushBack<std::deque<int>>_RMS | N/A | N/A | N/A | 1 | 1 | N/A | N/A | 
| BM_ContainerPushBack<std::list<int>>/1024 | 37.01 | 37.00 | 18909 | 1 | 1 | 110709823.50 | 27677455.87 | 
| BM_ContainerPushBack<std::list<int>>/4096 | 146.38 | 146.28 | 4311 | 1 | 1 | 112005277.45 | 28001319.36 | 
| BM_ContainerPushBack<std::list<int>>/32768 | 1540.03 | 1497.00 | 476 | 1 | 1 | 87556200.48 | 21889050.12 | 
| BM_ContainerPushBack<std::list<int>>/262144 | 11208.59 | 11183.77 | 62 | 1 | 1 | 93758688.42 | 23439672.11 | 
| BM_ContainerPushBack<std::list<int>>_BigO | N/A | N/A | N/A | 1 | 1 | N/A | N/A | 
| BM_ContainerPushBack<std::list<int>>_RMS | N/A | N/A | N/A | 1 | 1 | N/A | N/A | 


### Performance Across Container Sizes

The benchmark compares the time taken to insert elements into different containers, testing various container sizes to observe how each implementation scales.

Key metrics tracked:
- Items processed per second
- Bytes processed per second
- Big O computational complexity

## Complexity Analysis

Google Benchmark computed the following complexity estimations:

```
{{GBENCH_JSON:compute_complexity}}
```

## Assembly Analysis

Assembly for the vector implementation:

```asm
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
```

Assembly for the deque implementation:

```asm
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
```

Assembly for the list implementation:

```asm
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
```

## All Assembly Files

- [BM_ContainerPushBack<std::deque<int>>](#assembly-for-BM_ContainerPushBack<std::deque<int>>)
- [BM_ContainerPushBack<std::list<int>>](#assembly-for-BM_ContainerPushBack<std::list<int>>)
- [BM_ContainerPushBack<std::vector<int>>](#assembly-for-BM_ContainerPushBack<std::vector<int>>)
