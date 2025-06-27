	.file	"is_palindrome.c"
	.text
	.p2align 4
	.globl	is_palindrome
	.type	is_palindrome, @function
is_palindrome:
.LFB0:
	.cfi_startproc
	endbr64
	testl	%edi, %edi
	je	.L4
	movl	%edi, %edx
	xorl	%ecx, %ecx
	.p2align 4,,10
	.p2align 3
.L3:
	movslq	%edx, %rax
	leal	(%rcx,%rcx,4), %esi
	movl	%edx, %ecx
	imulq	$1717986919, %rax, %rax
	sarl	$31, %ecx
	sarq	$34, %rax
	subl	%ecx, %eax
	leal	(%rax,%rax,4), %ecx
	addl	%ecx, %ecx
	subl	%ecx, %edx
	leal	(%rdx,%rsi,2), %ecx
	movl	%eax, %edx
	testl	%eax, %eax
	jne	.L3
	xorl	%eax, %eax
	cmpl	%ecx, %edi
	sete	%al
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xorl	%ecx, %ecx
	xorl	%eax, %eax
	cmpl	%ecx, %edi
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
