	.file	"reverse_array.c"
	.text
	.p2align 4
	.globl	reverse_array
	.type	reverse_array, @function
reverse_array:
.LFB0:
	.cfi_startproc
	endbr64
	movq	%rdi, %rdx
	movl	%esi, %edi
	shrl	$31, %edi
	addl	%esi, %edi
	sarl	%edi
	cmpl	$1, %esi
	jle	.L1
	leal	-1(%rsi), %r9d
	cmpl	$3, %esi
	jle	.L3
	movslq	%esi, %r8
	movslq	%edi, %rax
	salq	$2, %r8
	salq	$2, %rax
	movq	%r8, %rcx
	subq	%rax, %rcx
	cmpq	%rcx, %rax
	jle	.L23
.L3:
	movslq	%r9d, %rax
	leaq	(%rdx,%rax,4), %rcx
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L11:
	movl	(%rcx), %r8d
	movl	(%rdx,%rax,4), %esi
	subq	$4, %rcx
	movl	%r8d, (%rdx,%rax,4)
	addq	$1, %rax
	movl	%esi, 4(%rcx)
	cmpl	%eax, %edi
	jg	.L11
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	movl	%edi, %r10d
	cmpl	$7, %esi
	jle	.L13
	movl	%edi, %esi
	movq	%rdx, %rax
	leaq	-16(%rdx,%r8), %rcx
	shrl	$2, %esi
	salq	$4, %rsi
	addq	%rdx, %rsi
	.p2align 4,,10
	.p2align 3
.L5:
	movdqu	(%rcx), %xmm2
	movdqu	(%rax), %xmm0
	addq	$16, %rax
	subq	$16, %rcx
	pshufd	$27, %xmm2, %xmm1
	pshufd	$27, %xmm0, %xmm0
	movups	%xmm1, -16(%rax)
	movups	%xmm0, 16(%rcx)
	cmpq	%rsi, %rax
	jne	.L5
	movl	%edi, %ecx
	andl	$-4, %ecx
	movl	%ecx, %eax
	cmpl	%ecx, %edi
	je	.L1
	subl	%ecx, %edi
	movl	%edi, %r10d
	cmpl	$1, %edi
	je	.L9
.L4:
	salq	$2, %rax
	subq	$8, %r8
	subq	%rax, %r8
	leaq	(%rdx,%rax), %rsi
	leaq	(%rdx,%r8), %rax
	movq	(%rsi), %xmm0
	movq	(%rax), %xmm1
	pshufd	$225, %xmm0, %xmm0
	pshufd	$225, %xmm1, %xmm1
	movq	%xmm1, (%rsi)
	movq	%xmm0, (%rax)
	testb	$1, %r10b
	je	.L1
	andl	$-2, %r10d
	addl	%r10d, %ecx
.L9:
	movslq	%ecx, %rax
	leaq	(%rdx,%rax,4), %rsi
	movl	%r9d, %eax
	subl	%ecx, %eax
	movl	(%rsi), %edi
	cltq
	leaq	(%rdx,%rax,4), %rax
	movl	(%rax), %edx
	movl	%edx, (%rsi)
	movl	%edi, (%rax)
	ret
.L13:
	xorl	%eax, %eax
	xorl	%ecx, %ecx
	jmp	.L4
	.cfi_endproc
.LFE0:
	.size	reverse_array, .-reverse_array
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
