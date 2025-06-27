	.file	"lcm.c"
	.text
	.globl	lcm
	.type	lcm, @function
lcm:
.LFB0:
	.cfi_startproc
	endbr64
	testl	%edi, %edi
	je	.L3
	testl	%esi, %esi
	je	.L3
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	%edi, %ebx
	xorl	%eax, %eax
	imull	%esi, %ebx
	call	gcd@PLT
	movl	%eax, %ecx
	movl	%ebx, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
	cltd
	idivl	%ecx
	ret
.L3:
	.cfi_restore 3
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	lcm, .-lcm
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
