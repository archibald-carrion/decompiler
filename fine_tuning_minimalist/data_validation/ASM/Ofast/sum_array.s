	.file	"sum_array.c"
	.text
	.p2align 4
	.globl	sum_array
	.type	sum_array, @function
sum_array:
.LFB0:
	.cfi_startproc
	endbr64
	movq	%rdi, %rcx
	testl	%esi, %esi
	jle	.L7
	leal	-1(%rsi), %eax
	cmpl	$2, %eax
	jbe	.L8
	movl	%esi, %edx
	movq	%rdi, %rax
	pxor	%xmm0, %xmm0
	shrl	$2, %edx
	salq	$4, %rdx
	addq	%rdi, %rdx
	.p2align 4,,10
	.p2align 3
.L4:
	movdqu	(%rax), %xmm2
	addq	$16, %rax
	paddd	%xmm2, %xmm0
	cmpq	%rdx, %rax
	jne	.L4
	movdqa	%xmm0, %xmm1
	movl	%esi, %edx
	psrldq	$8, %xmm1
	andl	$-4, %edx
	paddd	%xmm1, %xmm0
	movdqa	%xmm0, %xmm1
	psrldq	$4, %xmm1
	paddd	%xmm1, %xmm0
	movd	%xmm0, %eax
	testb	$3, %sil
	je	.L11
.L3:
	movslq	%edx, %rdi
	leaq	0(,%rdi,4), %r8
	addl	(%rcx,%rdi,4), %eax
	leal	1(%rdx), %edi
	cmpl	%edi, %esi
	jle	.L1
	addl	$2, %edx
	addl	4(%rcx,%r8), %eax
	cmpl	%edx, %esi
	jle	.L1
	addl	8(%rcx,%r8), %eax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	xorl	%eax, %eax
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	ret
.L8:
	xorl	%edx, %edx
	xorl	%eax, %eax
	jmp	.L3
	.cfi_endproc
.LFE0:
	.size	sum_array, .-sum_array
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
