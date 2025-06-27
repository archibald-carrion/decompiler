	.file	"is_palindrome.c"
	.text
	.globl	is_palindrome
	.type	is_palindrome, @function
is_palindrome:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%edi, %eax
	xorl	%edx, %edx
	movl	$10, %esi
.L2:
	testl	%eax, %eax
	je	.L5
	imull	$10, %edx, %ecx
	cltd
	idivl	%esi
	addl	%ecx, %edx
	jmp	.L2
.L5:
	xorl	%eax, %eax
	cmpl	%edi, %edx
	sete	%al
	ret
	.cfi_endproc
.LFE0:
	.size	is_palindrome, .-is_palindrome
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
