	.file	"fibonacci.c"
	.text
	.globl	fibonacci
	.type	fibonacci, @function
fibonacci:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	xorl	%ebp, %ebp
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	movl	%edi, %ebx
	pushq	%rcx
	.cfi_def_cfa_offset 32
.L3:
	cmpl	$1, %ebx
	jle	.L2
	leal	-1(%rbx), %edi
	subl	$2, %ebx
	call	fibonacci
	addl	%eax, %ebp
	jmp	.L3
.L2:
	leal	(%rbx,%rbp), %eax
	popq	%rdx
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
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
