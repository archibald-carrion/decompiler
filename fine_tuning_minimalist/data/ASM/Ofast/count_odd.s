	.file	"count_odd.c"
	.text
	.p2align 4
	.globl	count_odd
	.type	count_odd, @function
count_odd:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%esi, %ecx
	testl	%esi, %esi
	jle	.L11
	leal	-1(%rsi), %eax
	cmpl	$2, %eax
	jbe	.L12
	movl	%esi, %edx
	pxor	%xmm1, %xmm1
	movdqa	.LC0(%rip), %xmm3
	movq	%rdi, %rax
	shrl	$2, %edx
	movdqa	%xmm1, %xmm2
	salq	$4, %rdx
	addq	%rdi, %rdx
	.p2align 4,,10
	.p2align 3
.L4:
	movdqu	(%rax), %xmm0
	addq	$16, %rax
	pand	%xmm3, %xmm0
	pcmpeqd	%xmm2, %xmm0
	pcmpeqd	%xmm2, %xmm0
	psubd	%xmm0, %xmm1
	cmpq	%rax, %rdx
	jne	.L4
	movdqa	%xmm1, %xmm0
	movl	%ecx, %edx
	psrldq	$8, %xmm0
	andl	$-4, %edx
	paddd	%xmm0, %xmm1
	movdqa	%xmm1, %xmm0
	psrldq	$4, %xmm0
	paddd	%xmm0, %xmm1
	movd	%xmm1, %eax
	testb	$3, %cl
	je	.L19
.L3:
	movslq	%edx, %rsi
	leaq	0(,%rsi,4), %r8
	movl	(%rdi,%rsi,4), %esi
	andl	$1, %esi
	cmpl	$1, %esi
	leal	1(%rdx), %esi
	sbbl	$-1, %eax
	cmpl	%esi, %ecx
	jle	.L1
	movl	4(%rdi,%r8), %esi
	andl	$1, %esi
	cmpl	$1, %esi
	sbbl	$-1, %eax
	addl	$2, %edx
	cmpl	%edx, %ecx
	jle	.L1
	movl	8(%rdi,%r8), %edx
	andl	$1, %edx
	cmpl	$1, %edx
	sbbl	$-1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	xorl	%eax, %eax
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	ret
.L12:
	xorl	%edx, %edx
	xorl	%eax, %eax
	jmp	.L3
	.cfi_endproc
.LFE0:
	.size	count_odd, .-count_odd
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
