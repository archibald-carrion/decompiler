	.file	"count_char.c"
	.text
	.globl	count_char
	.type	count_char, @function
count_char:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
.L2:
	movb	(%rdi), %dl
	testb	%dl, %dl
	je	.L6
	cmpb	%sil, %dl
	jne	.L3
	incl	%eax
.L3:
	incq	%rdi
	jmp	.L2
.L6:
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
