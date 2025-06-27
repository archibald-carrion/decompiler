	.file	"reverse_digits.c"
	.text
	.p2align 4
	.globl	reverse_digits
	.type	reverse_digits, @function
reverse_digits:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%edx, %edx
	testl	%edi, %edi
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	movslq	%edi, %rax
	leal	(%rdx,%rdx,4), %ecx
	movl	%edi, %edx
	imulq	$1717986919, %rax, %rax
	sarl	$31, %edx
	sarq	$34, %rax
	subl	%edx, %eax
	leal	(%rax,%rax,4), %edx
	addl	%edx, %edx
	subl	%edx, %edi
	leal	(%rdi,%rcx,2), %edx
	movl	%eax, %edi
	testl	%eax, %eax
	jne	.L3
.L1:
	movl	%edx, %eax
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
