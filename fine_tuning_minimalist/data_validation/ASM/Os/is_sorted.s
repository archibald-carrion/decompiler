	.file	"is_sorted.c"
	.text
	.globl	is_sorted
	.type	is_sorted, @function
is_sorted:
.LFB0:
	.cfi_startproc
	endbr64
	movl	$1, %eax
.L2:
	cmpl	%eax, %esi
	jle	.L7
	movl	-4(%rdi,%rax,4), %edx
	incq	%rax
	cmpl	-4(%rdi,%rax,4), %edx
	jle	.L2
	xorl	%eax, %eax
	ret
.L7:
	movl	$1, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	is_sorted, .-is_sorted
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
