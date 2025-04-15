// Assembly:
0000000100003448 <BM_FloatAddition(benchmark::State&)>:
100003448:     	sub	sp, sp, #64
10000344c:     	stp	x22, x21, [sp, #16]
100003450:     	stp	x20, x19, [sp, #32]
100003454:     	stp	x29, x30, [sp, #48]
100003458:     	add	x29, sp, #48
10000345c:     	mov	x19, x0
100003460:     	str	wzr, [sp, #12]
100003464:     	ldr	w21, [x0, #28]
100003468:     	ldr	x20, [x0, #16]
100003478:     	b.eq	0x100003490 <BM_FloatAddition(benchmark::State&)+0x48>
10000347c:     	mov	w8, #1115947008
100003480:     	add	x9, sp, #12
100003484:     	str	w8, [sp, #12]
100003488:     	subs	x20, x20, #1
10000348c:     	b.ne	0x100003484 <BM_FloatAddition(benchmark::State&)+0x3c>
100003490:     	mov	x0, x19