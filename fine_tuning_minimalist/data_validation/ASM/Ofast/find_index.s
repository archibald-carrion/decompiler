	.file	"find_index.c"
	.text
	.p2align 4
	.globl	find_index
	.type	find_index, @function
find_index:
.LFB0:
	.cfi_startproc
	endbr64
	testl	%esi, %esi
	jle	.L5
	movslq	%esi, %rsi
	xorl	%eax, %eax
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L8:
	addq	$1, %rax
	cmpq	%rsi, %rax
	je	.L5
.L4:
	cmpl	%edx, (%rdi,%rax,4)
	jne	.L8
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	movl	$-1, %eax
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
