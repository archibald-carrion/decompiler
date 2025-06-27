	.file	"reverse_string.c"
	.text
	.p2align 4
	.globl	reverse_string
	.type	reverse_string, @function
reverse_string:
.LFB0:
	.cfi_startproc
	endbr64
	cmpb	$0, (%rdi)
	je	.L1
	leaq	1(%rdi), %rcx
	xorl	%edx, %edx
	.p2align 4,,10
	.p2align 3
.L3:
	addq	$1, %rcx
	movslq	%edx, %rax
	addl	$1, %edx
	cmpb	$0, -1(%rcx)
	jne	.L3
	sarl	%edx
	je	.L1
	movslq	%edx, %rdx
	addq	%rdi, %rax
	addq	%rdi, %rdx
	.p2align 4,,10
	.p2align 3
.L5:
	movzbl	(%rax), %esi
	movzbl	(%rdi), %ecx
	addq	$1, %rdi
	subq	$1, %rax
	movb	%sil, -1(%rdi)
	movb	%cl, 1(%rax)
	cmpq	%rdi, %rdx
	jne	.L5
.L1:
	ret
	.cfi_endproc
.LFE0:
	.size	reverse_string, .-reverse_string
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
