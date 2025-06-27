	.file	"is_sorted.c"
	.text
	.p2align 4
	.globl	is_sorted
	.type	is_sorted, @function
is_sorted:
.LFB0:
	.cfi_startproc
	endbr64
	cmpl	$1, %esi
	jle	.L4
	leal	-2(%rsi), %ecx
	movl	(%rdi), %edx
	leaq	4(%rdi), %rax
	leaq	8(%rdi,%rcx,4), %rsi
	jmp	.L3
	.p2align 4,,10
	.p2align 3
.L8:
	addq	$4, %rax
	cmpq	%rsi, %rax
	je	.L4
.L3:
	movl	%edx, %ecx
	movl	(%rax), %edx
	cmpl	%ecx, %edx
	jge	.L8
	xorl	%eax, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L4:
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
