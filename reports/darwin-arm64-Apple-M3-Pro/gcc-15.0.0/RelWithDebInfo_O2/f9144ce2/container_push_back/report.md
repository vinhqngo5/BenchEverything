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
| Timestamp          | 2025-04-16T17:17:42.394687 |
| Platform (Detailed) | darwin-arm64-Apple-M3-Pro |
| Compiler (Detailed) | gcc-15.0.0 |
| Build Flags        | RelWithDebInfo_O2 |
| Metadata Hash      | f9144ce2 |
| CPU Model          | Apple-M3-Pro |
| Compiler Type      | gcc |
| Compiler Version   | 15.0.0 |
| CMake Build Type   | RelWithDebInfo |
| CXX Flags Used     | -std=c++20 -O2 |


## Benchmark Results

### Raw Performance Data

| Benchmark | Time (ns) | CPU (ns) | Iterations | Items/s | Bytes/s | Unit | Threads | Reps |
| --------- | --------- | -------- | ---------- | ------- | ------- | ---- | ------- | ---- |
| BM_ContainerPushBack<std::vector<int>>/1024 | 1.84 | 1.70 | 412238 | 603278857.96 | 2413115431.83 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/4096 | 3.98 | 3.91 | 177452 | 1047519484.17 | 4190077936.68 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/32768 | 24.00 | 23.85 | 28364 | 1373837882.58 | 5495351530.33 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>/262144 | 471.88 | 305.14 | 2681 | 859081941.88 | 3436327767.54 | us | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::vector<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/1024 | 1.33 | 1.32 | 478786 | 778335848.00 | 3113343392.01 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/4096 | 4.24 | 3.92 | 188956 | 1044422101.22 | 4177688404.89 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/32768 | 24.12 | 23.76 | 30321 | 1378910132.55 | 5515640530.21 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>/262144 | 191.15 | 185.91 | 3890 | 1410068184.49 | 5640272737.96 | us | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_BigO | N/A | N/A | N/A | N/A | N/A | ns | 1 | 1 |
| BM_ContainerPushBack<std::deque<int>>_RMS | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/1024 | 39.79 | 37.91 | 18107 | 27013285.51 | 108053142.03 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/4096 | 153.71 | 149.29 | 4543 | 27436875.57 | 109747502.27 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/32768 | 1518.86 | 1480.60 | 492 | 22131635.12 | 88526540.49 | us | 1 | 1 |
| BM_ContainerPushBack<std::list<int>>/262144 | 11322.79 | 11178.77 | 62 | 23450156.11 | 93800624.46 | us | 1 | 1 |
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

// Assembly for benchmark function: BM_ContainerPushBack<std::vector<int>> (matched on 'BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>')
00000001000036a8 <void BM_ContainerPushBack<std::__1::vector<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
1000036a8:     	sub	sp, sp, #160
1000036ac:     	stp	x28, x27, [sp, #64]
1000036b0:     	stp	x26, x25, [sp, #80]
1000036b4:     	stp	x24, x23, [sp, #96]
1000036b8:     	stp	x22, x21, [sp, #112]
1000036bc:     	stp	x20, x19, [sp, #128]
1000036c0:     	stp	x29, x30, [sp, #144]
1000036c4:     	add	x29, sp, #144
1000036c8:     	mov	x23, x0
;     return this->__begin_[__n];
1000036cc:     	ldr	x8, [x0, #32]
;     return range_[pos];
1000036d0:     	ldr	x20, [x8]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
1000036d4:     	ldr	w19, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
1000036d8:     	ldr	x22, [x0, #16]
;   StartKeepRunning();
1000036dc:     	bl	0x100005d98 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
1000036e0:     	cmp	w19, #0
1000036e4:     	ccmp	x22, #0, #4, eq
1000036ec:     	str	x23, [sp]
;     --cached_;
1000036f4:     	subs	x22, x22, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
;         state.PauseTiming();
1000036fc:     	mov	x0, x23
100003700:     	bl	0x100005608 <benchmark::State::PauseTiming()>
;     pointer __end_ = nullptr;
100003704:     	stp	xzr, xzr, [sp, #32]
100003708:     	str	xzr, [sp, #48]
;         state.ResumeTiming();
10000370c:     	mov	x0, x23
100003710:     	bl	0x100005b10 <benchmark::State::ResumeTiming()>
;         for (int i = 0; i < N; ++i) {
100003714:     	cmp	w20, #1
10000371c:     	mov	x21, #0
100003720:     	mov	x27, #0
100003724:     	mov	x23, #0
100003728:     	mov	w25, #0
10000372c:     	ldr	x26, [sp, #32]
;   return ::new (std::__voidify(*__location)) _Tp(std::forward<_Args>(__args)...);
100003734:     	str	w25, [x27], #4
;       __v_.__end_ = __pos_;
100003738:     	str	x27, [sp, #40]
10000373c:     	mov	x19, x27
;         for (int i = 0; i < N; ++i) {
100003740:     	add	w25, w25, #1
100003744:     	mov	x27, x19
;         for (int i = 0; i < N; ++i) {
100003748:     	cmp	w25, w20
;     if (this->__end_ != this->__end_cap())
100003750:     	cmp	x27, x23
;         {return static_cast<size_type>(this->__end_ - this->__begin_);}
100003758:     	sub	x24, x27, x21
10000375c:     	asr	x23, x24, #2
;     __split_buffer<value_type, allocator_type&> __v(__recommend(size() + 1), size(), __a);
100003760:     	add	x8, x23, #1
;     if (__new_size > __ms)
100003764:     	lsr	x9, x8, #62
;     if (__cap >= __ms / 2)
10000376c:     	asr	x9, x24, #1
100003770:     	cmp	x9, x8
100003774:     	csel	x8, x9, x8, hi
100003778:     	mov	x9, #9223372036854775804
10000377c:     	cmp	x24, x9
100003780:     	mov	x9, #4611686018427387903
100003784:     	csel	x28, x8, x9, lo
;     if (__cap == 0) {

```

Assembly for the deque implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::deque<int>> (matched on 'BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>')
0000000100003b04 <void BM_ContainerPushBack<std::__1::deque<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003b04:     	sub	sp, sp, #160
100003b08:     	stp	x24, x23, [sp, #96]
100003b0c:     	stp	x22, x21, [sp, #112]
100003b10:     	stp	x20, x19, [sp, #128]
100003b14:     	stp	x29, x30, [sp, #144]
100003b18:     	add	x29, sp, #144
100003b1c:     	mov	x19, x0
;     return this->__begin_[__n];
100003b20:     	ldr	x8, [x0, #32]
;     return range_[pos];
100003b24:     	ldr	x20, [x8]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
100003b28:     	ldr	w22, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100003b2c:     	ldr	x21, [x0, #16]
;   StartKeepRunning();
100003b30:     	bl	0x100005d98 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100003b34:     	cmp	w22, #0
100003b38:     	ccmp	x21, #0, #4, eq
;     parent_->FinishKeepRunning();
100003b40:     	mov	x0, x19
100003b44:     	bl	0x100005e30 <benchmark::State::FinishKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(!started_, false)) {
100003b48:     	ldrb	w8, [x19, #24]
;     return max_iterations - total_iterations_ + batch_leftover_;
100003b50:     	ldp	x10, x8, [x19, #8]
100003b54:     	ldr	x9, [x19]
100003b58:     	sub	x8, x8, x9
100003b5c:     	add	x23, x8, x10
;     counters["items_per_second"] =
100003b60:     	add	x21, x19, #64
100003b64:     	mov	w8, #16

```

Assembly for the list implementation:

```asm

// Assembly for benchmark function: BM_ContainerPushBack<std::list<int>> (matched on 'BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>')
0000000100003e8c <void BM_ContainerPushBack<std::__1::list<int, std::__1::allocator<int>>>(benchmark::State&)>:
; static void BM_ContainerPushBack(benchmark::State& state) {
100003e8c:     	sub	sp, sp, #144
100003e90:     	stp	x26, x25, [sp, #64]
100003e94:     	stp	x24, x23, [sp, #80]
100003e98:     	stp	x22, x21, [sp, #96]
100003e9c:     	stp	x20, x19, [sp, #112]
100003ea0:     	stp	x29, x30, [sp, #128]
100003ea4:     	add	x29, sp, #128
100003ea8:     	mov	x19, x0
;     return this->__begin_[__n];
100003eac:     	ldr	x8, [x0, #32]
;     return range_[pos];
100003eb0:     	ldr	x20, [x8]
;   bool skipped() const { return internal::NotSkipped != skipped_; }
100003eb4:     	ldr	w22, [x0, #28]
;       : cached_(st->skipped() ? 0 : st->max_iterations), parent_(st) {}
100003eb8:     	ldr	x21, [x0, #16]
;   StartKeepRunning();
100003ebc:     	bl	0x100005d98 <benchmark::State::StartKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
100003ec0:     	cmp	w22, #0
100003ec4:     	ccmp	x21, #0, #4, eq
100003ecc:     	add	x22, sp, #32
;     --cached_;
100003ed4:     	subs	x21, x21, #1
;     if (BENCHMARK_BUILTIN_EXPECT(cached_ != 0, true)) return true;
;         state.PauseTiming();
100003edc:     	mov	x0, x19
100003ee0:     	bl	0x100005608 <benchmark::State::PauseTiming()>
;     __list_node_base() : __prev_(_NodeTraits::__unsafe_link_pointer_cast(__self())),
100003ee4:     	stp	x22, x22, [sp, #32]
;   explicit __compressed_pair_elem(_Up&& __u) : __value_(std::forward<_Up>(__u)) {}
100003ee8:     	str	xzr, [sp, #48]
;         state.ResumeTiming();
100003eec:     	mov	x0, x19
100003ef0:     	bl	0x100005b10 <benchmark::State::ResumeTiming()>
100003ef4:     	ldr	x24, [sp, #32]
100003ef8:     	ldr	x23, [sp, #48]
;         for (int i = 0; i < N; ++i) {
100003efc:     	cmp	w20, #1
100003f04:     	mov	x25, #0
;   return __builtin_operator_new(__args...);
100003f08:     	mov	w0, #24
100003f0c:     	bl	0x10002ed9c <_vsnprintf+0x10002ed9c>
;   return ::new (std::__voidify(*__location)) _Tp(std::forward<_Args>(__args)...);
100003f10:     	str	w25, [x0, #16]
;     __l->__next_ = base::__end_as_link();
100003f14:     	stp	x24, x22, [x0]
;     __f->__prev_->__next_ = __f;
100003f18:     	str	x0, [x24, #8]
;     ++base::__sz();
100003f1c:     	add	x8, x23, x25
100003f20:     	add	x8, x8, #1
;     base::__end_.__prev_ = __l;
100003f24:     	str	x0, [sp, #32]
;     ++base::__sz();
100003f28:     	str	x8, [sp, #48]
;         for (int i = 0; i < N; ++i) {
100003f2c:     	add	x25, x25, #1
100003f30:     	mov	x24, x0
;         for (int i = 0; i < N; ++i) {
100003f34:     	cmp	w20, w25
;     bool empty() const _NOEXCEPT {return __sz() == 0;}
100003f3c:     	add	x23, x23, x25
100003f40:     	mov	x24, x0
;     if (!empty())
;         __link_pointer __f = __end_.__next_;
100003f48:     	ldr	x0, [sp, #40]
;     __f->__prev_->__next_ = __l->__next_;
100003f4c:     	ldr	x8, [x24, #8]
100003f50:     	ldr	x9, [x0]
100003f54:     	str	x8, [x9, #8]
;     __l->__next_->__prev_ = __f->__prev_;
100003f58:     	ldr	x8, [x24, #8]
100003f5c:     	str	x9, [x8]
;         __sz() = 0;
100003f60:     	str	xzr, [sp, #48]
;         while (__f != __l)
100003f64:     	cmp	x0, x22
;             __f = __f->__next_;
100003f6c:     	ldr	x23, [x0, #8]
;   __builtin_operator_delete(__args...);
100003f70:     	bl	0x10002ed84 <_vsnprintf+0x10002ed84>
100003f74:     	mov	x0, x23
;         while (__f != __l)
100003f78:     	cmp	x23, x22
;     parent_->FinishKeepRunning();
100003f84:     	mov	x0, x19
100003f88:     	bl	0x100005e30 <benchmark::State::FinishKeepRunning()>
;     if (BENCHMARK_BUILTIN_EXPECT(!started_, false)) {
100003f8c:     	ldrb	w8, [x19, #24]
;     return max_iterations - total_iterations_ + batch_leftover_;
100003f94:     	ldp	x10, x8, [x19, #8]
100003f98:     	ldr	x9, [x19]
100003f9c:     	sub	x8, x8, x9
100003fa0:     	add	x23, x8, x10
;     counters["items_per_second"] =
100003fa4:     	add	x21, x19, #64
100003fa8:     	mov	w8, #16

```

## All Assembly Files

### Assembly Files

- [BM_ContainerPushBack<std::deque<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/RelWithDebInfo_O2/f9144ce2/container_push_back/assembly/BM_ContainerPushBack<std::deque<int>>.s)
- [BM_ContainerPushBack<std::list<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/RelWithDebInfo_O2/f9144ce2/container_push_back/assembly/BM_ContainerPushBack<std::list<int>>.s)
- [BM_ContainerPushBack<std::vector<int>>](../../../../../../results/darwin-arm64-Apple-M3-Pro/gcc-15.0.0/RelWithDebInfo_O2/f9144ce2/container_push_back/assembly/BM_ContainerPushBack<std::vector<int>>.s)
