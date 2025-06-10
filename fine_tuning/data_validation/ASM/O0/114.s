	.file	"114.c"
	.text
	.globl	_fseeki64
	.def	_fseeki64;	.scl	2;	.type	32;	.endef
	.seh_proc	_fseeki64
_fseeki64:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movq	%rdx, 24(%rbp)
	movl	%r8d, 32(%rbp)
	cmpl	$1, 32(%rbp)
	jne	.L2
	leaq	-8(%rbp), %rdx
	movq	16(%rbp), %rax
	movq	%rax, %rcx
	call	fgetpos
	testl	%eax, %eax
	je	.L3
	movl	$-1, %eax
	jmp	.L8
.L3:
	movq	-8(%rbp), %rdx
	movq	24(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -8(%rbp)
	jmp	.L5
.L2:
	cmpl	$2, 32(%rbp)
	jne	.L6
	movq	16(%rbp), %rax
	movq	%rax, %rcx
	call	fflush
	movq	16(%rbp), %rax
	movq	%rax, %rcx
	movq	__imp__fileno(%rip), %rax
	call	*%rax
	movl	%eax, %ecx
	movq	__imp__filelengthi64(%rip), %rax
	call	*%rax
	movq	24(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -8(%rbp)
	jmp	.L5
.L6:
	cmpl	$0, 32(%rbp)
	jne	.L7
	movq	24(%rbp), %rax
	movq	%rax, -8(%rbp)
	jmp	.L5
.L7:
	movq	__imp__errno(%rip), %rax
	call	*%rax
	movl	$22, (%rax)
	movl	$-1, %eax
	jmp	.L8
.L5:
	leaq	-8(%rbp), %rdx
	movq	16(%rbp), %rax
	movq	%rax, %rcx
	call	fsetpos
.L8:
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.globl	__imp__fseeki64
	.data
	.align 8
__imp__fseeki64:
	.quad	_fseeki64
	.text
	.globl	_ftelli64
	.def	_ftelli64;	.scl	2;	.type	32;	.endef
	.seh_proc	_ftelli64
_ftelli64:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	leaq	-8(%rbp), %rdx
	movq	16(%rbp), %rax
	movq	%rax, %rcx
	call	fgetpos
	testl	%eax, %eax
	je	.L10
	movq	$-1, %rax
	jmp	.L12
.L10:
	movq	-8(%rbp), %rax
.L12:
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.globl	__imp__ftelli64
	.data
	.align 8
__imp__ftelli64:
	.quad	_ftelli64
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
	.def	fgetpos;	.scl	2;	.type	32;	.endef
	.def	fflush;	.scl	2;	.type	32;	.endef
	.def	fsetpos;	.scl	2;	.type	32;	.endef
