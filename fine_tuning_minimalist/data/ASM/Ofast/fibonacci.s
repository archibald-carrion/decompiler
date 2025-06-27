	.file	"fibonacci.c"
	.text
	.p2align 4
	.globl	fibonacci
	.type	fibonacci, @function
fibonacci:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	movl	%edi, %r15d
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$104, %rsp
	.cfi_def_cfa_offset 160
	cmpl	$1, %edi
	jle	.L2
	leal	-1(%rdi), %eax
	movl	%edi, %r14d
	xorl	%ebx, %ebx
	movl	%eax, %edx
	movl	%eax, %r12d
	andl	$-2, %edx
	subl	%edx, %r14d
	movl	%r14d, %r13d
	cmpl	%r13d, %r15d
	je	.L3
.L72:
	subl	$2, %r15d
	movl	%r12d, %edi
	xorl	%ebp, %ebp
	movl	%r15d, %eax
	andl	$-2, %eax
	subl	%eax, %edi
	movl	%r12d, %eax
	movl	%ebx, %r12d
	movl	%r15d, %ebx
	movl	%edi, 56(%rsp)
.L32:
	movl	56(%rsp), %edi
	leal	-1(%rax), %edx
	movl	%edx, %r15d
	cmpl	%edi, %eax
	je	.L4
.L71:
	subl	$2, %eax
	movl	%r15d, %edi
	xorl	%r14d, %r14d
	movl	%eax, %edx
	movl	%eax, 36(%rsp)
	andl	$-2, %edx
	subl	%edx, %edi
	movl	%r15d, %edx
	movl	%r13d, %r15d
	movl	%r12d, %r13d
	movl	%edi, 60(%rsp)
.L29:
	movl	60(%rsp), %eax
	leal	-1(%rdx), %esi
	movl	%esi, %r8d
	cmpl	%eax, %edx
	je	.L5
	subl	$2, %edx
	movl	%r8d, %eax
	movl	%r14d, 44(%rsp)
	xorl	%r12d, %r12d
	movl	%edx, %esi
	movl	%edx, 48(%rsp)
	andl	$-2, %esi
	movl	%ebp, 40(%rsp)
	movl	%r13d, %ebp
	movl	%ebx, %r13d
	subl	%esi, %eax
	movl	%r15d, %ebx
	movl	%eax, 64(%rsp)
.L26:
	movl	64(%rsp), %eax
	leal	-1(%r8), %esi
	movl	%esi, %r10d
	cmpl	%eax, %r8d
	je	.L6
	leal	-2(%r8), %esi
	movl	%r10d, %r15d
	xorl	%r14d, %r14d
	movl	%ebx, %edx
	movl	%esi, %ecx
	movl	%esi, 52(%rsp)
	movl	%ebp, %esi
	andl	$-2, %ecx
	subl	%ecx, %r15d
	movl	%r12d, %ecx
	movl	%r13d, %r12d
	movl	%r10d, %r13d
.L23:
	leal	-1(%r13), %r8d
	movl	%r8d, %ebx
	cmpl	%r15d, %r13d
	je	.L7
.L68:
	subl	$2, %r13d
	movl	%r8d, %r10d
	xorl	%ebp, %ebp
	movl	%edx, %r8d
	movl	%r13d, %eax
	movl	%r13d, 4(%rsp)
	movl	%ebx, %edx
	andl	$-2, %eax
	subl	%eax, %r10d
	.p2align 4,,10
	.p2align 3
.L20:
	leal	-1(%rdx), %eax
	movl	%eax, %ebx
	cmpl	%r10d, %edx
	je	.L8
	leal	-2(%rdx), %edi
	leal	-5(%rdx), %r11d
	movl	%edi, %eax
	leal	-4(%rdx), %r9d
	leal	-3(%rdx), %r13d
	movl	%ebx, %edx
	andl	$-2, %eax
	movl	%r9d, 8(%rsp)
	movl	%r11d, %r9d
	subl	%eax, %edx
	xorl	%eax, %eax
	movl	%edx, 28(%rsp)
	movl	%eax, %r11d
	movl	%r13d, %eax
.L17:
	movl	28(%rsp), %edx
	cmpl	%edx, %ebx
	je	.L9
	movl	%eax, %edx
	leal	-4(%rbx), %r13d
	movl	%esi, 16(%rsp)
	movl	%edi, %esi
	andl	$-2, %edx
	movl	%ecx, 20(%rsp)
	movl	%eax, %ecx
	subl	%edx, %r13d
	movl	8(%rsp), %edx
	movl	%r12d, 24(%rsp)
	movl	%ebx, %r12d
	movl	%r13d, 12(%rsp)
	leal	-6(%rbx), %r13d
	andl	$-2, %edx
	movl	$0, (%rsp)
	subl	%edx, %r13d
	movl	%r13d, 32(%rsp)
	movl	%r9d, %r13d
	leal	2(%r13), %edx
	cmpl	%r13d, 12(%rsp)
	je	.L10
.L65:
	xorl	%ebx, %ebx
.L11:
	leal	-1(%rdx), %edi
	movl	%esi, 92(%rsp)
	movl	%ecx, 88(%rsp)
	movl	%r9d, 84(%rsp)
	movl	%r10d, 80(%rsp)
	movl	%r8d, 76(%rsp)
	movl	%r11d, 72(%rsp)
	movl	%edx, 68(%rsp)
	call	fibonacci
	movl	68(%rsp), %edx
	movl	72(%rsp), %r11d
	addl	%eax, %ebx
	movl	76(%rsp), %r8d
	movl	80(%rsp), %r10d
	subl	$2, %edx
	movl	84(%rsp), %r9d
	movl	88(%rsp), %ecx
	cmpl	$1, %edx
	movl	92(%rsp), %esi
	jg	.L11
	movl	%r13d, %eax
	andl	$1, %eax
	addl	%ebx, %eax
	addl	%eax, (%rsp)
	leal	-2(%r13), %eax
	cmpl	%eax, 32(%rsp)
	je	.L64
	movl	%eax, %r13d
	leal	2(%r13), %edx
	cmpl	%r13d, 12(%rsp)
	jne	.L65
.L10:
	movl	(%rsp), %r13d
	movl	%r12d, %ebx
	movl	%ecx, %eax
	movl	%esi, %edi
	movl	20(%rsp), %ecx
	movl	16(%rsp), %esi
	movl	24(%rsp), %r12d
	addl	%r13d, %edx
.L13:
	subl	$2, %ebx
	subl	$2, 8(%rsp)
	addl	%edx, %r11d
	subl	$2, %eax
	subl	$2, %r9d
	cmpl	$1, %ebx
	jne	.L17
	movl	%r11d, %eax
	movl	%edi, %edx
	addl	$1, %eax
	addl	%eax, %ebp
	cmpl	$1, %edi
	jne	.L20
	movl	4(%rsp), %r13d
	movl	%r8d, %edx
	addl	$1, %ebp
.L69:
	addl	%ebp, %r14d
	cmpl	$1, %r13d
	jne	.L23
.L67:
	movl	%esi, %ebp
	movl	52(%rsp), %esi
	movl	%r12d, %r13d
	movl	%edx, %ebx
	movl	%ecx, %r12d
	addl	$1, %r14d
.L22:
	movl	%esi, %r8d
	addl	%r14d, %r12d
	cmpl	$1, %esi
	jne	.L26
	movl	%ebx, %r15d
	movl	44(%rsp), %r14d
	movl	%r13d, %ebx
	movl	48(%rsp), %edx
	movl	%ebp, %r13d
	movl	40(%rsp), %ebp
	addl	$1, %r12d
.L25:
	addl	%r12d, %r14d
	cmpl	$1, %edx
	jne	.L29
	movl	36(%rsp), %eax
	addl	$1, %r14d
	movl	%r13d, %r12d
	movl	%r15d, %r13d
	addl	%r14d, %ebp
	cmpl	$1, %eax
	jne	.L32
.L70:
	movl	%ebx, %r15d
	addl	$1, %ebp
	movl	%r12d, %ebx
	addl	%ebp, %ebx
	cmpl	$1, %r15d
	jne	.L66
.L52:
	leal	1(%rbx), %r15d
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L8:
	movl	4(%rsp), %r13d
	addl	%eax, %ebp
	movl	%r8d, %edx
	addl	%ebp, %r14d
	cmpl	$1, %r13d
	je	.L67
	leal	-1(%r13), %r8d
	movl	%r8d, %ebx
	cmpl	%r15d, %r13d
	jne	.L68
.L7:
	movl	%esi, %ebp
	movl	%r12d, %r13d
	movl	52(%rsp), %esi
	movl	%edx, %ebx
	movl	%ecx, %r12d
	addl	%r8d, %r14d
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L9:
	leal	-1(%rbx,%r11), %eax
	movl	%edi, %edx
	addl	%eax, %ebp
	cmpl	$1, %edi
	jne	.L20
	movl	4(%rsp), %r13d
	movl	%r8d, %edx
	addl	$1, %ebp
	jmp	.L69
.L6:
	movl	%ebx, %r15d
	movl	44(%rsp), %r14d
	movl	%r13d, %ebx
	movl	48(%rsp), %edx
	movl	%ebp, %r13d
	addl	%esi, %r12d
	movl	40(%rsp), %ebp
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L64:
	movl	(%rsp), %edx
	movl	%r12d, %ebx
	movl	%ecx, %eax
	movl	%esi, %edi
	movl	20(%rsp), %ecx
	movl	16(%rsp), %esi
	movl	24(%rsp), %r12d
	leal	1(%rdx,%r13), %edx
	jmp	.L13
.L5:
	movl	36(%rsp), %eax
	addl	%esi, %r14d
	movl	%r13d, %r12d
	movl	%r15d, %r13d
	addl	%r14d, %ebp
	cmpl	$1, %eax
	je	.L70
	movl	56(%rsp), %edi
	leal	-1(%rax), %edx
	movl	%edx, %r15d
	cmpl	%edi, %eax
	jne	.L71
.L4:
	movl	%ebx, %r15d
	addl	%edx, %ebp
	movl	%r12d, %ebx
	addl	%ebp, %ebx
	cmpl	$1, %r15d
	je	.L52
.L66:
	leal	-1(%r15), %eax
	movl	%eax, %r12d
	cmpl	%r13d, %r15d
	jne	.L72
.L3:
	leal	(%rax,%rbx), %r15d
.L2:
	addq	$104, %rsp
	.cfi_def_cfa_offset 56
	movl	%r15d, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE0:
	.size	fibonacci, .-fibonacci
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
