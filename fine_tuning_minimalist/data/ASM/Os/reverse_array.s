	.file	"reverse_array.c"
	.text
	.globl	reverse_array
	.type	reverse_array, @function
reverse_array:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%esi, %eax
	movl	$2, %ecx
	movslq	%esi, %rsi
	cltd
	idivl	%ecx
	leaq	(%rdi,%rsi,4), %rcx
	xorl	%edx, %edx
.L2:
	subq	$4, %rcx
	cmpl	%edx, %eax
	jle	.L5
	movl	(%rdi,%rdx,4), %esi
	movl	(%rcx), %r8d
	movl	%r8d, (%rdi,%rdx,4)
	incq	%rdx
	movl	%esi, (%rcx)
	jmp	.L2
.L5:
	ret
	.cfi_endproc
.LFE0:
	.size	reverse_array, .-reverse_array
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
