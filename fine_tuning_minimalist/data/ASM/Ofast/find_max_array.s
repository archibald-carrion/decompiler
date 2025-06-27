	.file	"find_max_array.c"
	.text
	.p2align 4
	.globl	find_max_array
	.type	find_max_array, @function
find_max_array:
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
	movd	%eax, %xmm3
	movq	%rdi, %rax
	shrl	$2, %edx
	pshufd	$0, %xmm3, %xmm0
	salq	$4, %rdx
	addq	%rdi, %rdx
	.p2align 4,,10
	.p2align 3
.L4:
	movdqu	4(%rax), %xmm1
	addq	$16, %rax
	movdqa	%xmm1, %xmm2
	pcmpgtd	%xmm0, %xmm2
	pand	%xmm2, %xmm1
	pandn	%xmm0, %xmm2
	movdqa	%xmm2, %xmm0
	por	%xmm1, %xmm0
	cmpq	%rdx, %rax
	jne	.L4
	movdqa	%xmm0, %xmm2
	psrldq	$8, %xmm2
	movdqa	%xmm2, %xmm1
	pcmpgtd	%xmm0, %xmm1
	pand	%xmm1, %xmm2
	pandn	%xmm0, %xmm1
	por	%xmm2, %xmm1
	movdqa	%xmm1, %xmm2
	psrldq	$4, %xmm2
	movdqa	%xmm2, %xmm0
	pcmpgtd	%xmm1, %xmm0
	pand	%xmm0, %xmm2
	pandn	%xmm1, %xmm0
	por	%xmm2, %xmm0
	movd	%xmm0, %eax
	testb	$3, %cl
	je	.L1
	andl	$-4, %ecx
	addl	$1, %ecx
.L3:
	movslq	%ecx, %rdx
	leaq	0(,%rdx,4), %r8
	movl	(%rdi,%rdx,4), %edx
	cmpl	%edx, %eax
	cmovl	%edx, %eax
	leal	1(%rcx), %edx
	cmpl	%edx, %esi
	jle	.L1
	movl	4(%rdi,%r8), %edx
	cmpl	%edx, %eax
	cmovl	%edx, %eax
	addl	$2, %ecx
	cmpl	%ecx, %esi
	jle	.L1
	movl	8(%rdi,%r8), %edx
	cmpl	%edx, %eax
	cmovl	%edx, %eax
.L1:
	ret
.L7:
	movl	$1, %ecx
	jmp	.L3
	.cfi_endproc
.LFE0:
	.size	find_max_array, .-find_max_array
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
