	.file	"find_min_array.c"
	.text
	.p2align 4
	.globl	find_min_array
	.type	find_min_array, @function
find_min_array:
.LFB0:
	.cfi_startproc
	endbr64
	movl	(%rdi), %eax
	cmpl	$1, %esi
	jle	.L1
	leal	-2(%rsi), %edx
	leal	-1(%rsi), %ecx
	cmpl	$2, %edx
	jbe	.L7
	movl	%ecx, %edx
	movd	%eax, %xmm4
	movq	%rdi, %rax
	shrl	$2, %edx
	pshufd	$0, %xmm4, %xmm0
	salq	$4, %rdx
	addq	%rdi, %rdx
	.p2align 4,,10
	.p2align 3
.L4:
	movdqu	4(%rax), %xmm1
	movdqu	4(%rax), %xmm3
	addq	$16, %rax
	pcmpgtd	%xmm0, %xmm1
	pand	%xmm1, %xmm0
	pandn	%xmm3, %xmm1
	por	%xmm1, %xmm0
	cmpq	%rdx, %rax
	jne	.L4
	movdqa	%xmm0, %xmm2
	psrldq	$8, %xmm2
	movdqa	%xmm2, %xmm1
	pcmpgtd	%xmm0, %xmm1
	pand	%xmm1, %xmm0
	pandn	%xmm2, %xmm1
	por	%xmm1, %xmm0
	movdqa	%xmm0, %xmm2
	psrldq	$4, %xmm2
	movdqa	%xmm2, %xmm1
	pcmpgtd	%xmm0, %xmm1
	pand	%xmm1, %xmm0
	pandn	%xmm2, %xmm1
	por	%xmm0, %xmm1
	movd	%xmm1, %eax
	testb	$3, %cl
	je	.L1
	andl	$-4, %ecx
	addl	$1, %ecx
.L3:
	movslq	%ecx, %rdx
	leaq	0(,%rdx,4), %r8
	movl	(%rdi,%rdx,4), %edx
	cmpl	%edx, %eax
	cmovg	%edx, %eax
	leal	1(%rcx), %edx
	cmpl	%edx, %esi
	jle	.L1
	movl	4(%rdi,%r8), %edx
	cmpl	%edx, %eax
	cmovg	%edx, %eax
	addl	$2, %ecx
	cmpl	%ecx, %esi
	jle	.L1
	movl	8(%rdi,%r8), %edx
	cmpl	%edx, %eax
	cmovg	%edx, %eax
.L1:
	ret
.L7:
	movl	$1, %ecx
	jmp	.L3
	.cfi_endproc
.LFE0:
	.size	find_min_array, .-find_min_array
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
