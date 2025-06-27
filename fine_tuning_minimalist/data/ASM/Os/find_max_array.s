	.file	"find_max_array.c"
	.text
	.globl	find_max_array
	.type	find_max_array, @function
find_max_array:
.LFB0:
	.cfi_startproc
	endbr64
	movl	(%rdi), %eax
	xorl	%edx, %edx
.L2:
	incq	%rdx
	cmpl	%edx, %esi
	jle	.L5
	movl	(%rdi,%rdx,4), %ecx
	cmpl	%ecx, %eax
	cmovl	%ecx, %eax
	jmp	.L2
.L5:
	ret
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
