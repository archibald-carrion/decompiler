	.file	"100011.c"
	.text
	.def	__scan_uint;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_uint
__scan_uint:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movl	$10, %edi
	movq	%rcx, %rbx
	movl	%edx, %esi
	testl	$1, %r8d
	jne	.L2
	movl	$16, %edi
	testl	$2, %r8d
	jne	.L2
	andl	$4, %r8d
	movl	$8, %edi
	jne	.L2
	movq	(%rcx), %rax
	movl	$10, %edi
	cmpb	$48, (%rax)
	jne	.L2
	leaq	1(%rax), %rdx
	movq	%rdx, (%rcx)
	movb	1(%rax), %dl
	andl	$-33, %edx
	cmpb	$88, %dl
	je	.L3
	decl	%esi
	movl	$8, %edi
	jmp	.L2
.L3:
	addq	$2, %rax
	subl	$2, %esi
	movl	$16, %edi
	movq	%rax, (%rcx)
.L2:
	xorl	%ebp, %ebp
.L4:
	movq	(%rbx), %rax
	movl	%edi, %edx
	movsbl	(%rax), %ecx
	call	__isbdigit
	testl	%eax, %eax
	je	.L1
	movq	(%rbx), %rax
	imull	%edi, %ebp
	movl	%edi, %edx
	movsbl	(%rax), %ecx
	call	__digit
	incq	(%rbx)
	addl	%eax, %ebp
	decl	%esi
	jne	.L4
.L1:
	movl	%ebp, %eax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.seh_endproc
	.def	__scan_int;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_int
__scan_int:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	(%rcx), %rax
	decl	%edx
	cmpb	$45, (%rax)
	je	.L19
	addq	$40, %rsp
	jmp	__scan_uint
.L19:
	incq	%rax
	movq	%rax, (%rcx)
	call	__scan_uint
	negl	%eax
	addq	$40, %rsp
	ret
	.seh_endproc
	.def	__scan_str.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_str.isra.0
__scan_str.isra.0:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	xorl	%ebx, %ebx
	movq	%rcx, %rsi
	movl	%edx, %edi
.L21:
	cmpl	%ebx, %edi
	jle	.L22
	movq	(%rsi), %rax
	movsbl	(%rax,%rbx), %ecx
	movl	%ecx, %ebp
	call	*__imp_isspace(%rip)
	movl	%eax, %edx
	leaq	1(%rbx), %rax
	testl	%edx, %edx
	jne	.L22
	testb	%bpl, %bpl
	je	.L22
	movq	%rax, %rbx
	jmp	.L21
.L22:
	leal	1(%rbx), %ecx
	movl	%ebx, %edi
	movslq	%ecx, %rcx
	call	malloc
	xorl	%edx, %edx
.L24:
	cmpl	%edx, %edi
	jle	.L26
	movq	(%rsi), %rcx
	movb	(%rcx), %r8b
	incq	%rcx
	movq	%rcx, (%rsi)
	movb	%r8b, (%rax,%rdx)
	incq	%rdx
	jmp	.L24
.L26:
	movb	$0, (%rax,%rbx)
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.seh_endproc
	.globl	vsscanf
	.def	vsscanf;	.scl	2;	.type	32;	.endef
	.seh_proc	vsscanf
vsscanf:
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$64, %rsp
	.seh_stackalloc	64
	.seh_endprologue
	xorl	%edi, %edi
	leaq	.L46(%rip), %rbp
	movq	%rcx, 112(%rsp)
	movq	%rdx, %rbx
	movq	%r8, %rsi
.L28:
	movb	(%rbx), %al
	testb	%al, %al
	je	.L27
	cmpb	$32, %al
	jne	.L74
.L29:
	movq	112(%rsp), %r12
	movsbl	(%r12), %ecx
	call	*__imp_isspace(%rip)
	testl	%eax, %eax
	je	.L32
	incq	%r12
	movq	%r12, 112(%rsp)
	jmp	.L29
.L74:
	cmpb	$37, %al
	jne	.L33
	cmpb	$42, 1(%rbx)
	je	.L34
	incq	%rbx
	xorl	%r8d, %r8d
	jmp	.L35
.L34:
	addq	$2, %rbx
	movl	$32, %r8d
.L35:
	movsbl	(%rbx), %eax
	orl	$-1, %edx
	subl	$48, %eax
	cmpl	$9, %eax
	ja	.L36
	movq	%rbx, %rcx
	movl	%r8d, 44(%rsp)
	call	atoi
	movl	44(%rsp), %r8d
	movl	%eax, %edx
.L37:
	movsbl	(%rbx), %eax
	subl	$48, %eax
	cmpl	$9, %eax
	ja	.L36
	incq	%rbx
	jmp	.L37
.L36:
	movb	(%rbx), %al
	cmpb	$108, %al
	jne	.L39
	orl	$64, %r8d
	jmp	.L75
.L39:
	cmpb	$76, %al
	jne	.L40
	orb	$-128, %r8b
.L75:
	incq	%rbx
.L40:
	movb	(%rbx), %al
	cmpb	$115, %al
	jg	.L41
	cmpb	$98, %al
	jg	.L42
	cmpb	$88, %al
	jne	.L27
	orl	$16, %r8d
	jmp	.L52
.L42:
	subl	$99, %eax
	cmpb	$16, %al
	ja	.L27
	movzbl	%al, %eax
	movslq	0(%rbp,%rax,4), %rax
	addq	%rbp, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L46:
	.long	.L51-.L46
	.long	.L50-.L46
	.long	.L27-.L46
	.long	.L49-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L76-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L47-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L27-.L46
	.long	.L69-.L46
	.text
.L41:
	cmpb	$120, %al
	je	.L52
	jmp	.L27
.L50:
	orl	$1, %r8d
.L76:
	movl	$1, %eax
	jmp	.L45
.L52:
	orl	$2, %r8d
	jmp	.L77
.L47:
	orl	$4, %r8d
.L77:
	movl	$2, %eax
	jmp	.L45
.L51:
	movl	$5, %eax
	jmp	.L45
.L49:
	movl	$3, %eax
	jmp	.L45
.L69:
	movl	$4, %eax
.L45:
	testl	$32, %r8d
	je	.L53
	cmpl	$4, %eax
	je	.L54
	cmpl	$5, %eax
	je	.L55
	cmpl	$2, %eax
	je	.L56
	cmpl	$3, %eax
	je	.L57
	leaq	112(%rsp), %rcx
	call	__scan_int
	jmp	.L66
.L56:
	leaq	112(%rsp), %rcx
	call	__scan_uint
	jmp	.L66
.L57:
	movq	112(%rsp), %rdx
	leaq	48(%rsp), %rcx
	leaq	112(%rsp), %r8
	call	strtold
	jmp	.L66
.L54:
	leaq	112(%rsp), %rcx
	call	__scan_str.isra.0
	movq	%rax, %rcx
	call	free
	jmp	.L66
.L55:
	incq	112(%rsp)
	jmp	.L66
.L53:
	movq	(%rsi), %r12
	cmpl	$4, %eax
	je	.L59
	cmpl	$5, %eax
	je	.L60
	cmpl	$2, %eax
	je	.L61
	cmpl	$3, %eax
	je	.L62
	leaq	112(%rsp), %rcx
	call	__scan_int
	jmp	.L78
.L61:
	leaq	112(%rsp), %rcx
	call	__scan_uint
.L78:
	movl	%eax, (%r12)
	jmp	.L63
.L62:
	testl	$64, %r8d
	movq	112(%rsp), %rdx
	leaq	48(%rsp), %rcx
	je	.L64
	leaq	112(%rsp), %r8
	call	strtold
	fldt	48(%rsp)
	fstpl	(%r12)
	jmp	.L63
.L64:
	andb	$-128, %r8b
	leaq	112(%rsp), %r8
	je	.L65
	call	strtold
	fldt	48(%rsp)
	fstpt	(%r12)
	jmp	.L63
.L65:
	call	strtold
	fldt	48(%rsp)
	fstps	(%r12)
.L63:
	addq	$8, %rsi
	jmp	.L66
.L59:
	leaq	112(%rsp), %rcx
	call	__scan_str.isra.0
	movq	%rax, (%r12)
	jmp	.L63
.L60:
	movq	112(%rsp), %rax
	movb	(%rax), %dl
	incq	%rax
	movq	%rax, 112(%rsp)
	movb	%dl, (%r12)
	jmp	.L63
.L66:
	incl	%edi
	jmp	.L32
.L33:
	movq	112(%rsp), %rdx
	cmpb	%al, (%rdx)
	jne	.L27
	incq	%rdx
	incq	%rbx
	movq	%rdx, 112(%rsp)
.L32:
	incq	%rbx
	jmp	.L28
.L27:
	movl	%edi, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
	.def	__isbdigit;	.scl	2;	.type	32;	.endef
	.def	__digit;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	atoi;	.scl	2;	.type	32;	.endef
	.def	strtold;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
