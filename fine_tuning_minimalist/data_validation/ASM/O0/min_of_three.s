	.file	"min_of_three.c"
	.text
	.globl	min_of_three
	.type	min_of_three, @function
min_of_three:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movl	-20(%rbp), %eax
	movl	%eax, -4(%rbp)
	movl	-24(%rbp), %eax
	cmpl	-4(%rbp), %eax
	jge	.L2
	movl	-24(%rbp), %eax
	movl	%eax, -4(%rbp)
.L2:
	movl	-28(%rbp), %eax
	cmpl	-4(%rbp), %eax
	jge	.L3
	movl	-28(%rbp), %eax
	movl	%eax, -4(%rbp)
.L3:
	movl	-4(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	min_of_three, .-min_of_three
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
