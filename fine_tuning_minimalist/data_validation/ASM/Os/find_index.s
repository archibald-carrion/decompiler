	.file	"find_index.c"
	.text
	.globl	find_index
	.type	find_index, @function
find_index:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
.L2:
	cmpl	%eax, %esi
	jle	.L7
	leaq	1(%rax), %rcx
	cmpl	%edx, (%rdi,%rax,4)
	je	.L1
	movq	%rcx, %rax
	jmp	.L2
.L7:
	orl	$-1, %eax
.L1:
	ret
	.cfi_endproc
.LFE0:
	.size	find_index, .-find_index
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
