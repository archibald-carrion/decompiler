	.file	"to_upper.c"
	.text
	.p2align 4
	.globl	to_upper
	.type	to_upper, @function
to_upper:
.LFB0:
	.cfi_startproc
	endbr64
	movzbl	(%rdi), %eax
	testb	%al, %al
	je	.L14
	.p2align 4,,10
	.p2align 3
.L5:
	leal	-97(%rax), %edx
	cmpb	$25, %dl
	ja	.L3
	subl	$32, %eax
	addq	$1, %rdi
	movb	%al, -1(%rdi)
	movzbl	(%rdi), %eax
	testb	%al, %al
	jne	.L5
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	movzbl	1(%rdi), %eax
	addq	$1, %rdi
	testb	%al, %al
	jne	.L5
.L14:
	ret
	.cfi_endproc
.LFE0:
	.size	to_upper, .-to_upper
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
