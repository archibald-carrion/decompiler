	.file	"sum_even.c"
	.text
	.globl	sum_even
	.type	sum_even, @function
sum_even:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
	xorl	%edx, %edx
.L2:
	cmpl	%eax, %esi
	jle	.L6
	movl	(%rdi,%rax,4), %ecx
	testb	$1, %cl
	jne	.L3
	addl	%ecx, %edx
.L3:
	incq	%rax
	jmp	.L2
.L6:
	movl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	sum_even, .-sum_even
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
