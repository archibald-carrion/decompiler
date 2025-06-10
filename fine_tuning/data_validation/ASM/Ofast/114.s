	.file	"114.c"
	.text
	.p2align 4
	.globl	_ftelli64
	.def	_ftelli64;	.scl	2;	.type	32;	.endef
	.seh_proc	_ftelli64
_ftelli64:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	40(%rsp), %rdx
	call	fgetpos
	testl	%eax, %eax
	jne	.L3
	movq	40(%rsp), %rax
.L1:
	addq	$56, %rsp
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	movq	$-1, %rax
	jmp	.L1
	.seh_endproc
	.p2align 4
	.globl	_fseeki64
	.def	_fseeki64;	.scl	2;	.type	32;	.endef
	.seh_proc	_fseeki64
_fseeki64:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	movq	%rcx, %rsi
	movq	%rdx, %rbx
	cmpl	$1, %r8d
	je	.L14
	cmpl	$2, %r8d
	je	.L15
	testl	%r8d, %r8d
	jne	.L13
	leaq	56(%rsp), %rdx
.L8:
	movq	%rsi, %rcx
	movq	%rbx, 56(%rsp)
	call	fsetpos
.L5:
	addq	$72, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L14:
	leaq	56(%rsp), %rdx
	movq	%rdx, 40(%rsp)
	call	fgetpos
	testl	%eax, %eax
	jne	.L7
	movq	40(%rsp), %rdx
	addq	56(%rsp), %rbx
	jmp	.L8
	.p2align 4,,10
	.p2align 3
.L15:
	call	fflush
	movq	%rsi, %rcx
	call	*__imp__fileno(%rip)
	movl	%eax, %ecx
	call	*__imp__filelengthi64(%rip)
	leaq	56(%rsp), %rdx
	addq	%rax, %rbx
	jmp	.L8
.L13:
	call	*__imp__errno(%rip)
	movl	$22, (%rax)
.L7:
	movl	$-1, %eax
	jmp	.L5
	.seh_endproc
	.globl	__imp__ftelli64
	.data
	.align 8
__imp__ftelli64:
	.quad	_ftelli64
	.globl	__imp__fseeki64
	.align 8
__imp__fseeki64:
	.quad	_fseeki64
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
	.def	fgetpos;	.scl	2;	.type	32;	.endef
	.def	fsetpos;	.scl	2;	.type	32;	.endef
	.def	fflush;	.scl	2;	.type	32;	.endef
