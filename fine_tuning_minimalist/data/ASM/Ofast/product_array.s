	.file	"product_array.c"
	.text
	.p2align 4
	.globl	product_array
	.type	product_array, @function
product_array:
.LFB0:
	.cfi_startproc
	endbr64
	movq	%rdi, %rcx
	testl	%esi, %esi
	jle	.L8
	leal	-1(%rsi), %eax
	cmpl	$26, %eax
	jbe	.L9
	movl	%esi, %edx
	movdqa	.LC0(%rip), %xmm1
	movq	%rdi, %rax
	shrl	$2, %edx
	salq	$4, %rdx
	addq	%rdi, %rdx
	.p2align 4,,10
	.p2align 3
.L4:
	movdqu	(%rax), %xmm2
	movdqu	(%rax), %xmm0
	addq	$16, %rax
	pmuludq	%xmm1, %xmm2
	psrlq	$32, %xmm0
	psrlq	$32, %xmm1
	pmuludq	%xmm1, %xmm0
	pshufd	$8, %xmm2, %xmm1
	pshufd	$8, %xmm0, %xmm0
	punpckldq	%xmm0, %xmm1
	cmpq	%rdx, %rax
	jne	.L4
	movdqa	%xmm1, %xmm0
	movl	%esi, %eax
	psrldq	$8, %xmm0
	andl	$-4, %eax
	movdqa	%xmm0, %xmm2
	psrlq	$32, %xmm0
	pmuludq	%xmm1, %xmm2
	psrlq	$32, %xmm1
	pmuludq	%xmm1, %xmm0
	pshufd	$8, %xmm2, %xmm1
	pshufd	$8, %xmm0, %xmm0
	punpckldq	%xmm0, %xmm1
	movdqa	%xmm1, %xmm0
	psrldq	$4, %xmm0
	pmuludq	%xmm1, %xmm0
	movd	%xmm0, %edx
	testb	$3, %sil
	je	.L1
.L3:
	cltq
	movq	%rax, %rdi
	imull	(%rcx,%rax,4), %edx
	addq	$1, %rax
	notq	%rdi
	addl	%esi, %edi
	andl	$1, %edi
	cmpl	%eax, %esi
	jle	.L1
	testl	%edi, %edi
	je	.L7
	imull	(%rcx,%rax,4), %edx
	addq	$1, %rax
	cmpl	%eax, %esi
	jle	.L1
	.p2align 4,,10
	.p2align 3
.L7:
	imull	(%rcx,%rax,4), %edx
	imull	4(%rcx,%rax,4), %edx
	addq	$2, %rax
	cmpl	%eax, %esi
	jg	.L7
.L1:
	movl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	movl	$1, %edx
	movl	%edx, %eax
	ret
.L9:
	xorl	%eax, %eax
	movl	$1, %edx
	jmp	.L3
	.cfi_endproc
.LFE0:
	.size	product_array, .-product_array
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC0:
	.long	1
	.long	1
	.long	1
	.long	1
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
