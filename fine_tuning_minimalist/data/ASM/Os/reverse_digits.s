	.file	"reverse_digits.c"
	.text
	.globl	reverse_digits
	.type	reverse_digits, @function
reverse_digits:
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
	imull	$10, %ecx, %ecx
	idivl	%esi
	addl	%edx, %ecx
	jmp	.L2
.L5:
	movl	%ecx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	reverse_digits, .-reverse_digits
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
