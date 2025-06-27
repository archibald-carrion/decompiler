	.file	"is_prime.c"
	.text
	.p2align 4
	.globl	is_prime
	.type	is_prime, @function
is_prime:
.LFB0:
	.cfi_startproc
	endbr64
	xorl	%esi, %esi
	cmpl	$1, %edi
	jle	.L1
	cmpl	$3, %edi
	jle	.L6
	movl	%edi, %esi
	andl	$1, %esi
	je	.L1
	movl	$2, %ecx
	jmp	.L3
	.p2align 4,,10
	.p2align 3
.L4:
	movl	%edi, %eax
	cltd
	idivl	%ecx
	testl	%edx, %edx
	je	.L7
.L3:
	addl	$1, %ecx
	movl	%ecx, %eax
	imull	%ecx, %eax
	cmpl	%edi, %eax
	jle	.L4
.L1:
	movl	%esi, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	xorl	%esi, %esi
	movl	%esi, %eax
	ret
.L6:
	movl	$1, %esi
	jmp	.L1
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
