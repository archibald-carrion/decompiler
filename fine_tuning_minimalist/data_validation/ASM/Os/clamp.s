	.file	"clamp.c"
	.text
	.globl	clamp
	.type	clamp, @function
clamp:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%esi, %eax
	cmpl	%esi, %edi
	jl	.L2
	cmpl	%edx, %edi
	movl	%edx, %eax
	cmovle	%edi, %eax
.L2:
	ret
	.cfi_endproc
.LFE0:
	.size	clamp, .-clamp
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
