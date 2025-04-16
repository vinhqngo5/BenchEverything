# Container Push Back Performance Benchmark

This benchmark compares the performance of `push_back` operations for different C++ containers:
- `std::vector<int>`
- `std::deque<int>`
- `std::list<int>`

The benchmark measures how performance scales across different container sizes, from 1,024 to 262,144 elements.

## Environment

| Property           | Value |
|--------------------|-------|
| Experiment Name    | container_push_back |
| Timestamp          | 2025-04-16T17:14:52.304599 |
| Platform (Detailed) | darwin-arm64-Apple-M3-Pro |
| Compiler (Detailed) | gcc-15.0.0 |
| Build Flags        | Release_O3 |
| Metadata Hash      | f7343e8a |
| CPU Model          | Apple-M3-Pro |
| Compiler Type      | gcc |
| Compiler Version   | 15.0.0 |
| CMake Build Type   | Release |
| CXX Flags Used     | -std=c++20 -O3 |


## Benchmark Results

### Raw Performance Data

| Benchmark | Time (ns) | CPU (ns) | Iterations | Items/s | Bytes/s | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ------- | ------- | ---- | ------- | ---- |
| BM_ContainerPushBack<std::vector<int>>/1024 | 1.29 | 1.29 | 539853 | 793959621.93 | 3175838487.71 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/4096 | 2.38 | 2.38 | 295743 | 1719733851.99 | 6878935407.94 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/32768 | 12.24 | 12.24 | 55675 | 2676872782.55 | 10707491130.20 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/262144 | 152.35 | 152.23 | 4658 | 1722070421.92 | 6888281687.68 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/1024 | 1.32 | 1.22 | 598367 | 836610683.06 | 3346442732.25 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/4096 | 3.27 | 3.27 | 220650 | 1252747837.66 | 5010991350.63 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/32768 | 21.23 | 20.84 | 33040 | 1572433008.68 | 6289732034.71 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/262144 | 165.74 | 165.24 | 3513 | 1586447021.21 | 6345788084.83 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/1024 | 36.41 | 36.07 | 16673 | 28385613.96 | 113542455.84 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/4096 | 139.50 | 139.41 | 4917 | 29380275.57 | 117521102.27 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/32768 | 1469.44 | 1427.32 | 497 | 22957776.98 | 91831107.90 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/262144 | 10621.86 | 10593.18 | 66 | 24746483.59 | 98985934.35 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |


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

```

Assembly for the deque implementation:

```asm

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

```

Assembly for the list implementation:

```asm

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

```

## All Assembly Files

### Assembly Files

- [BM_ContainerPushBack<std::deque<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/f7343e8a/container_push_back/assembly/BM_ContainerPushBack<std::deque<int>>.s)
- [BM_ContainerPushBack<std::list<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/f7343e8a/container_push_back/assembly/BM_ContainerPushBack<std::list<int>>.s)
- [BM_ContainerPushBack<std::vector<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/Release_O3/f7343e8a/container_push_back/assembly/BM_ContainerPushBack<std::vector<int>>.s)
