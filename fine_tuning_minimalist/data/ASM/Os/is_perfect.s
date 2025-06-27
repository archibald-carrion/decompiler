	.file	"is_perfect.c"
	.text
	.globl	is_perfect
	.type	is_perfect, @function
is_perfect:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%edi, %eax
	movl	$2, %ecx
	movl	$1, %esi
	cltd
	idivl	%ecx
	movl	%eax, %r8d
.L2:
	cmpl	%ecx, %r8d
	jl	.L6
	movl	%edi, %eax
	cltd
	idivl	%ecx
	testl	%edx, %edx
	jne	.L3
	addl	%ecx, %esi
.L3:
	incl	%ecx
	jmp	.L2
.L6:
	cmpl	$1, %edi
	setg	%dl
	xorl	%eax, %eax
	cmpl	%edi, %esi
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
