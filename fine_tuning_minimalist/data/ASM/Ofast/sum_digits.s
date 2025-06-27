	.file	"sum_digits.c"
	.text
	.p2align 4
	.globl	sum_digits
	.type	sum_digits, @function
sum_digits:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%ecx, %ecx
	testl	%edi, %edi
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	movslq	%edi, %rax
	movl	%edi, %edx
	imulq	$1717986919, %rax, %rax
	sarl	$31, %edx
	sarq	$34, %rax
	subl	%edx, %eax
	leal	(%rax,%rax,4), %edx
	addl	%edx, %edx
	subl	%edx, %edi
	addl	%edi, %ecx
	movl	%eax, %edi
	testl	%eax, %eax
	jne	.L3
.L1:
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
