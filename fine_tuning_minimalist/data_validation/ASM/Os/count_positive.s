	.file	"count_positive.c"
	.text
	.globl	count_positive
	.type	count_positive, @function
count_positive:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
	xorl	%edx, %edx
.L2:
	cmpl	%eax, %esi
	jle	.L6
	cmpl	$0, (%rdi,%rax,4)
	jle	.L3
	incl	%edx
.L3:
	incq	%rax
	jmp	.L2
.L6:
	movl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	count_positive, .-count_positive
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
