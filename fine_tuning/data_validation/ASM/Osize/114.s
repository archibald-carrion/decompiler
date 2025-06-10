	.file	"114.c"
	.text
	.globl	_ftelli64
	.def	_ftelli64;	.scl	2;	.type	32;	.endef
	.seh_proc	_ftelli64
_ftelli64:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	40(%rsp), %rdx
	call	fgetpos
	movl	%eax, %edx
	orq	$-1, %rax
	testl	%edx, %edx
	jne	.L1
	movq	40(%rsp), %rax
.L1:
	addq	$56, %rsp
	ret
	.seh_endproc
	.globl	_fseeki64
	.def	_fseeki64;	.scl	2;	.type	32;	.endef
	.seh_proc	_fseeki64
_fseeki64:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rsi
	movq	%rdx, %rbx
	cmpl	$1, %r8d
	jne	.L6
	leaq	40(%rsp), %rdx
	call	fgetpos
	testl	%eax, %eax
	jne	.L7
	addq	40(%rsp), %rbx
	jmp	.L8
.L6:
	cmpl	$2, %r8d
	jne	.L9
	call	fflush
	movq	%rsi, %rcx
	call	*__imp__fileno(%rip)
	movl	%eax, %ecx
	call	*__imp__filelengthi64(%rip)
	addq	%rax, %rbx
	jmp	.L8
.L9:
	testl	%r8d, %r8d
	je	.L8
	call	*__imp__errno(%rip)
	movl	$22, (%rax)
.L7:
	orl	$-1, %eax
	jmp	.L5
.L8:
	leaq	40(%rsp), %rdx
	movq	%rsi, %rcx
	movq	%rbx, 40(%rsp)
	call	fsetpos
.L5:
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
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
	.def	fflush;	.scl	2;	.type	32;	.endef
	.def	fsetpos;	.scl	2;	.type	32;	.endef
