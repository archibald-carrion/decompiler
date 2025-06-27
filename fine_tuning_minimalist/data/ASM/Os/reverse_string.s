	.file	"reverse_string.c"
	.text
	.globl	reverse_string
	.type	reverse_string, @function
reverse_string:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movq	%rdi, %rbx
	call	strlen@PLT
	xorl	%edx, %edx
	movl	%eax, %ecx
	cltq
	sarl	%ecx
	addq	%rbx, %rax
.L2:
	decq	%rax
	cmpl	%edx, %ecx
	jle	.L6
	movb	(%rbx,%rdx), %sil
	movb	(%rax), %dil
	movb	%dil, (%rbx,%rdx)
	incq	%rdx
	movb	%sil, (%rax)
	jmp	.L2
.L6:
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE0:
	.size	reverse_string, .-reverse_string
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
