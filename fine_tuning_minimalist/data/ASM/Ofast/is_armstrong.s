	.file	"is_armstrong.c"
	.text
	.p2align 4
	.globl	is_armstrong
	.type	is_armstrong, @function
is_armstrong:
.LFB0:
	.cfi_startproc
	endbr64
	movl	%edi, %r10d
	testl	%edi, %edi
	je	.L6
	movl	%edi, %edx
	xorl	%esi, %esi
	.p2align 4,,10
	.p2align 3
.L3:
	movslq	%edx, %rax
	sarl	$31, %edx
	movl	%esi, %edi
	leal	1(%rsi), %esi
	imulq	$1717986919, %rax, %rax
	sarq	$34, %rax
	subl	%edx, %eax
	movl	%eax, %edx
	jne	.L3
	xorl	%r11d, %r11d
	movl	%r10d, %r9d
	.p2align 4,,10
	.p2align 3
.L4:
	movslq	%r9d, %r8
	movl	%r9d, %eax
	movl	$1, %edx
	imulq	$1717986919, %r8, %rsi
	sarl	$31, %eax
	sarq	$34, %rsi
	subl	%eax, %esi
	leal	(%rsi,%rsi,4), %eax
	movl	%r9d, %esi
	addl	%eax, %eax
	subl	%eax, %esi
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L5:
	movl	%eax, %ecx
	imull	%esi, %edx
	addl	$1, %eax
	cmpl	%ecx, %edi
	jne	.L5
	imulq	$1717986919, %r8, %r8
	movl	%r9d, %eax
	addl	%edx, %r11d
	sarl	$31, %eax
	sarq	$34, %r8
	movl	%r8d, %r9d
	subl	%eax, %r9d
	jne	.L4
	xorl	%eax, %eax
	cmpl	%r11d, %r10d
	sete	%al
	ret
.L6:
	xorl	%r11d, %r11d
	xorl	%eax, %eax
	cmpl	%r11d, %r10d
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
