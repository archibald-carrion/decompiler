	.file	"count_even.c"
	.text
	.globl	count_even
	.type	count_even, @function
count_even:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
	xorl	%edx, %edx
.L2:
	cmpl	%eax, %esi
	jle	.L6
	movl	(%rdi,%rax,4), %ecx
	andl	$1, %ecx
	cmpl	$1, %ecx
	adcl	$0, %edx
	incq	%rax
	jmp	.L2
.L6:
	movl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	count_even, .-count_even
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
