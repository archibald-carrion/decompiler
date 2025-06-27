	.file	"find_char.c"
	.text
	.p2align 4
	.globl	find_char
	.type	find_char, @function
find_char:
.LFB0:
	.cfi_startproc
	endbr64
	movzbl	(%rdi), %edx
	testb	%dl, %dl
	je	.L5
	xorl	%eax, %eax
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L8:
	addq	$1, %rax
	movzbl	(%rdi,%rax), %edx
	testb	%dl, %dl
	je	.L5
.L4:
	cmpb	%dl, %sil
	jne	.L8
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	movl	$-1, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	find_char, .-find_char
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
