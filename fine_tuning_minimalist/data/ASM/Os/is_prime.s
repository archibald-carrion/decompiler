	.file	"is_prime.c"
	.text
	.globl	is_prime
	.type	is_prime, @function
is_prime:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%eax, %eax
	movl	$2, %ecx
	cmpl	$1, %edi
	jle	.L1
.L3:
	movl	%ecx, %eax
	imull	%ecx, %eax
	cmpl	%edi, %eax
	jg	.L10
	movl	%edi, %eax
	cltd
	idivl	%ecx
	movl	%edx, %eax
	testl	%edx, %edx
	je	.L1
	incl	%ecx
	jmp	.L3
.L10:
	movl	$1, %eax
.L1:
	ret
	.cfi_endproc
.LFE0:
	.size	is_prime, .-is_prime
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
