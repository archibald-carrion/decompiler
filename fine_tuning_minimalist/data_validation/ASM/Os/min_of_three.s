	.file	"min_of_three.c"
	.text
	.globl	min_of_three
	.type	min_of_three, @function
min_of_three:
.LFB0:
	.cfi_startproc
	endbr64
	cmpl	%edx, %esi
	movl	%edi, %eax
	cmovg	%edx, %esi
	cmpl	%edi, %esi
	cmovle	%esi, %eax
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
