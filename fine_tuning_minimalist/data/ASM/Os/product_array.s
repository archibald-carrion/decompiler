	.file	"product_array.c"
	.text
	.globl	product_array
	.type	product_array, @function
product_array:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
	movl	$1, %edx
.L2:
	cmpl	%eax, %esi
	jle	.L5
	imull	(%rdi,%rax,4), %edx
	incq	%rax
	jmp	.L2
.L5:
	movl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	product_array, .-product_array
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
