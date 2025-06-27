	.file	"is_armstrong.c"
	.text
	.globl	is_armstrong
	.type	is_armstrong, @function
is_armstrong:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%edi, %eax
	xorl	%r10d, %r10d
	movl	$10, %ecx
.L2:
	testl	%eax, %eax
	je	.L9
	cltd
	incl	%r10d
	idivl	%ecx
	jmp	.L2
.L9:
	xorl	%r8d, %r8d
	movl	%edi, %ecx
	movl	$10, %esi
.L4:
	testl	%ecx, %ecx
	je	.L6
	movl	%ecx, %eax
	xorl	%r9d, %r9d
	cltd
	idivl	%esi
	movl	$1, %eax
.L7:
	cmpl	%r9d, %r10d
	je	.L10
	imull	%edx, %eax
	incl	%r9d
	jmp	.L7
.L10:
	addl	%eax, %r8d
	movl	%ecx, %eax
	cltd
	idivl	%esi
	movl	%eax, %ecx
	jmp	.L4
.L6:
	xorl	%eax, %eax
	cmpl	%edi, %r8d
	sete	%al
	ret
	.cfi_endproc
.LFE0:
	.size	is_armstrong, .-is_armstrong
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
