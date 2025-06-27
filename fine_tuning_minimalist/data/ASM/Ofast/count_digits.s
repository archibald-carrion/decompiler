	.file	"count_digits.c"
	.text
	.p2align 4
	.globl	count_digits
	.type	count_digits, @function
count_digits:
.LFB0:
	.cfi_startproc
	endbr64
	movl	$1, %ecx
	testl	%edi, %edi
	je	.L1
	xorl	%ecx, %ecx
	.p2align 4,,10
	.p2align 3
.L3:
	movslq	%edi, %rax
	movl	%edi, %edx
	addl	$1, %ecx
	imulq	$1717986919, %rax, %rax
	sarl	$31, %edx
	sarq	$34, %rax
	subl	%edx, %eax
	movl	%eax, %edi
	jne	.L3
.L1:
	movl	%ecx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	count_digits, .-count_digits
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
