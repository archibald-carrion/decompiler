	.file	"sum_digits.c"
	.text
	.globl	sum_digits
	.type	sum_digits, @function
sum_digits:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%edi, %eax
	xorl	%ecx, %ecx
	movl	$10, %esi
.L2:
	testl	%eax, %eax
	je	.L5
	cltd
	idivl	%esi
	addl	%edx, %ecx
	jmp	.L2
.L5:
	movl	%ecx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	sum_digits, .-sum_digits
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
