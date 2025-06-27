	.file	"swap_no_temp.c"
	.text
	.globl	swap_no_temp
	.type	swap_no_temp, @function
swap_no_temp:
.LFB0:
	.cfi_startproc
	endbr64
	movl	(%rsi), %eax
	addl	(%rdi), %eax
	movl	%eax, (%rdi)
	subl	(%rsi), %eax
	movl	%eax, (%rsi)
	subl	%eax, (%rdi)
	ret
	.cfi_endproc
.LFE0:
	.size	swap_no_temp, .-swap_no_temp
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
