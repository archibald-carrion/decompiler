	.file	"count_char.c"
	.text
	.p2align 4
	.globl	count_char
	.type	count_char, @function
count_char:
.LFB0:
	.cfi_startproc
	endbr64
	movzbl	(%rdi), %eax
	testb	%al, %al
	je	.L5
	addq	$1, %rdi
	xorl	%edx, %edx
	.p2align 4,,10
	.p2align 3
.L4:
	cmpb	%al, %sil
	sete	%al
	addq	$1, %rdi
	movzbl	%al, %eax
	addl	%eax, %edx
	movzbl	-1(%rdi), %eax
	testb	%al, %al
	jne	.L4
	movl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	xorl	%edx, %edx
	movl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	count_char, .-count_char
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
