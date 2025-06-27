	.file	"strlen.c"
	.text
	.p2align 4
	.globl	strlen
	.type	strlen, @function
strlen:
.LFB0:
	.cfi_startproc
	endbr64
	cmpb	$0, (%rdi)
	je	.L3
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	addq	$1, %rdi
	call	strlen@PLT
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
	addl	$1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	strlen, .-strlen
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
