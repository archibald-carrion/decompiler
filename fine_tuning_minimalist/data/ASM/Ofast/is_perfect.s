	.file	"is_perfect.c"
	.text
	.p2align 4
	.globl	is_perfect
	.type	is_perfect, @function
is_perfect:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%edi, %r8d
	shrl	$31, %r8d
	addl	%edi, %r8d
	sarl	%r8d
	cmpl	$3, %edi
	jle	.L5
	movl	$2, %ecx
	movl	$1, %esi
	.p2align 4,,10
	.p2align 3
.L4:
	movl	%edi, %eax
	cltd
	idivl	%ecx
	leal	(%rsi,%rcx), %eax
	testl	%edx, %edx
	cmove	%eax, %esi
	addl	$1, %ecx
	cmpl	%r8d, %ecx
	jle	.L4
	cmpl	$1, %edi
	setg	%dl
	xorl	%eax, %eax
	cmpl	%esi, %edi
	sete	%al
	andl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	cmpl	$1, %edi
	movl	$1, %esi
	setg	%dl
	xorl	%eax, %eax
	cmpl	%esi, %edi
	sete	%al
	andl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	is_perfect, .-is_perfect
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
