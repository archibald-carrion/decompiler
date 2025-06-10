	.file	"100011.c"
	.text
	.def	__scan_uint;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_uint
__scan_uint:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movl	%edx, 24(%rbp)
	movl	%r8d, 32(%rbp)
	movl	32(%rbp), %eax
	andl	$1, %eax
	testl	%eax, %eax
	je	.L2
	movl	$10, -4(%rbp)
	jmp	.L3
.L2:
	movl	32(%rbp), %eax
	andl	$2, %eax
	testl	%eax, %eax
	je	.L4
	movl	$16, -4(%rbp)
	jmp	.L3
.L4:
	movl	32(%rbp), %eax
	andl	$4, %eax
	testl	%eax, %eax
	je	.L5
	movl	$8, -4(%rbp)
	jmp	.L3
.L5:
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	cmpb	$48, %al
	jne	.L6
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
	subl	$1, 24(%rbp)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	cmpb	$120, %al
	je	.L7
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	cmpb	$88, %al
	jne	.L8
.L7:
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
	subl	$1, 24(%rbp)
	movl	$16, -4(%rbp)
	jmp	.L3
.L8:
	movl	$8, -4(%rbp)
	jmp	.L3
.L6:
	movl	$10, -4(%rbp)
.L3:
	movl	$0, -8(%rbp)
	jmp	.L10
.L12:
	movl	-4(%rbp), %eax
	movl	-8(%rbp), %edx
	imull	%edx, %eax
	movl	%eax, -8(%rbp)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	movl	-4(%rbp), %edx
	movl	%eax, %ecx
	call	__digit
	addl	%eax, -8(%rbp)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
	subl	$1, 24(%rbp)
	cmpl	$0, 24(%rbp)
	jne	.L10
	movl	-8(%rbp), %eax
	jmp	.L11
.L10:
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	movl	-4(%rbp), %edx
	movl	%eax, %ecx
	call	__isbdigit
	testl	%eax, %eax
	jne	.L12
	movl	-8(%rbp), %eax
.L11:
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.def	__scan_int;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_int
__scan_int:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movl	%edx, 24(%rbp)
	movl	%r8d, 32(%rbp)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	cmpb	$45, %al
	jne	.L14
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	movl	32(%rbp), %ecx
	movq	16(%rbp), %rax
	movl	%ecx, %r8d
	movq	%rax, %rcx
	call	__scan_uint
	negl	%eax
	jmp	.L15
.L14:
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	movl	32(%rbp), %ecx
	movq	16(%rbp), %rax
	movl	%ecx, %r8d
	movq	%rax, %rcx
	call	__scan_uint
.L15:
	addq	$32, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.def	__scan_str;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_str
__scan_str:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movl	%edx, 24(%rbp)
	movl	%r8d, 32(%rbp)
	movl	$0, -4(%rbp)
	jmp	.L17
.L19:
	movq	16(%rbp), %rax
	movq	(%rax), %rdx
	movl	-4(%rbp), %eax
	cltq
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	movl	%eax, %ecx
	movq	__imp_isspace(%rip), %rax
	call	*%rax
	testl	%eax, %eax
	jne	.L18
	movq	16(%rbp), %rax
	movq	(%rax), %rdx
	movl	-4(%rbp), %eax
	cltq
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	je	.L18
	addl	$1, -4(%rbp)
.L17:
	movl	-4(%rbp), %eax
	cmpl	24(%rbp), %eax
	jl	.L19
.L18:
	movl	-4(%rbp), %eax
	addl	$1, %eax
	cltq
	movq	%rax, %rcx
	call	malloc
	movq	%rax, -16(%rbp)
	movl	$0, -8(%rbp)
	jmp	.L20
.L21:
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movl	-8(%rbp), %edx
	movslq	%edx, %rcx
	movq	-16(%rbp), %rdx
	addq	%rcx, %rdx
	movzbl	(%rax), %eax
	movb	%al, (%rdx)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
	addl	$1, -8(%rbp)
.L20:
	movl	-8(%rbp), %eax
	cmpl	-4(%rbp), %eax
	jl	.L21
	movl	-8(%rbp), %eax
	movslq	%eax, %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movb	$0, (%rax)
	movq	-16(%rbp), %rax
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.def	__scan_char;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_char
__scan_char:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$16, %rsp
	.seh_stackalloc	16
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movl	%edx, 24(%rbp)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	movb	%al, -1(%rbp)
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
	movzbl	-1(%rbp), %eax
	addq	$16, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.def	__scan_float;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_float
__scan_float:
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
	movq	24(%rbp), %rax
	movq	(%rax), %rdx
	leaq	-16(%rbp), %rax
	movq	24(%rbp), %rcx
	movq	%rcx, %r8
	movq	%rax, %rcx
	call	strtold
	fldt	-16(%rbp)
	movq	16(%rbp), %rax
	fstpt	(%rax)
	movq	16(%rbp), %rax
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.def	__scan_space;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_space
__scan_space:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	jmp	.L28
.L29:
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	leaq	1(%rax), %rdx
	movq	16(%rbp), %rax
	movq	%rdx, (%rax)
.L28:
	movq	16(%rbp), %rax
	movq	(%rax), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	movl	%eax, %ecx
	movq	__imp_isspace(%rip), %rax
	call	*%rax
	testl	%eax, %eax
	jne	.L29
	nop
	nop
	addq	$32, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.globl	vsscanf
	.def	vsscanf;	.scl	2;	.type	32;	.endef
	.seh_proc	vsscanf
vsscanf:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$144, %rsp
	.seh_stackalloc	144
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movq	%rdx, 24(%rbp)
	movq	%r8, 32(%rbp)
	movl	$0, -12(%rbp)
	jmp	.L31
.L73:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$32, %al
	jne	.L32
	leaq	16(%rbp), %rcx
	call	__scan_space
	jmp	.L33
.L32:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$37, %al
	jne	.L34
	movl	$0, -4(%rbp)
	addq	$1, 24(%rbp)
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$42, %al
	jne	.L35
	orl	$32, -4(%rbp)
	addq	$1, 24(%rbp)
.L35:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	subl	$48, %eax
	cmpl	$9, %eax
	ja	.L36
	movq	24(%rbp), %rax
	movq	%rax, %rcx
	call	atoi
	movl	%eax, -8(%rbp)
	jmp	.L37
.L38:
	addq	$1, 24(%rbp)
.L37:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	subl	$48, %eax
	cmpl	$9, %eax
	jbe	.L38
	jmp	.L39
.L36:
	movl	$-1, -8(%rbp)
.L39:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$108, %al
	jne	.L40
	orl	$64, -4(%rbp)
	addq	$1, 24(%rbp)
	jmp	.L41
.L40:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$76, %al
	jne	.L41
	orl	$128, -4(%rbp)
	addq	$1, 24(%rbp)
.L41:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	subl	$88, %eax
	cmpl	$32, %eax
	ja	.L42
	movl	%eax, %eax
	leaq	0(,%rax,4), %rdx
	leaq	.L44(%rip), %rax
	movl	(%rdx,%rax), %eax
	cltq
	leaq	.L44(%rip), %rdx
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L44:
	.long	.L51-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L50-.L44
	.long	.L49-.L44
	.long	.L42-.L44
	.long	.L48-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L47-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L46-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L45-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L42-.L44
	.long	.L43-.L44
	.text
.L49:
	orl	$1, -4(%rbp)
	movl	$1, -16(%rbp)
	jmp	.L52
.L47:
	movl	$1, -16(%rbp)
	jmp	.L52
.L51:
	orl	$16, -4(%rbp)
.L43:
	orl	$2, -4(%rbp)
	movl	$2, -16(%rbp)
	jmp	.L52
.L46:
	orl	$4, -4(%rbp)
	movl	$2, -16(%rbp)
	jmp	.L52
.L45:
	movl	$4, -16(%rbp)
	jmp	.L52
.L50:
	movl	$5, -16(%rbp)
	jmp	.L52
.L48:
	movl	$3, -16(%rbp)
	jmp	.L52
.L42:
	movl	-12(%rbp), %eax
	jmp	.L53
.L52:
	movl	-4(%rbp), %eax
	andl	$32, %eax
	testl	%eax, %eax
	je	.L54
	cmpl	$5, -16(%rbp)
	ja	.L62
	movl	-16(%rbp), %eax
	leaq	0(,%rax,4), %rdx
	leaq	.L57(%rip), %rax
	movl	(%rdx,%rax), %eax
	cltq
	leaq	.L57(%rip), %rdx
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L57:
	.long	.L62-.L57
	.long	.L61-.L57
	.long	.L60-.L57
	.long	.L59-.L57
	.long	.L58-.L57
	.long	.L56-.L57
	.text
.L61:
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_int
	jmp	.L62
.L60:
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_uint
	jmp	.L62
.L59:
	leaq	-96(%rbp), %rax
	movl	-4(%rbp), %edx
	movl	%edx, %r8d
	leaq	16(%rbp), %rdx
	movq	%rax, %rcx
	call	__scan_float
	jmp	.L62
.L58:
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_str
	movq	%rax, %rcx
	call	free
	jmp	.L62
.L56:
	movl	-4(%rbp), %eax
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_char
	jmp	.L62
.L54:
	cmpl	$5, -16(%rbp)
	ja	.L62
	movl	-16(%rbp), %eax
	leaq	0(,%rax,4), %rdx
	leaq	.L64(%rip), %rax
	movl	(%rdx,%rax), %eax
	cltq
	leaq	.L64(%rip), %rdx
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L64:
	.long	.L62-.L64
	.long	.L68-.L64
	.long	.L67-.L64
	.long	.L66-.L64
	.long	.L65-.L64
	.long	.L63-.L64
	.text
.L68:
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -72(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_int
	movq	-72(%rbp), %rdx
	movl	%eax, (%rdx)
	jmp	.L62
.L67:
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -64(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_uint
	movq	-64(%rbp), %rdx
	movl	%eax, (%rdx)
	jmp	.L62
.L66:
	movl	-4(%rbp), %eax
	andl	$64, %eax
	testl	%eax, %eax
	je	.L69
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -56(%rbp)
	leaq	-96(%rbp), %rax
	movl	-4(%rbp), %edx
	movl	%edx, %r8d
	leaq	16(%rbp), %rdx
	movq	%rax, %rcx
	call	__scan_float
	fldt	-96(%rbp)
	fstpl	-104(%rbp)
	movsd	-104(%rbp), %xmm0
	movq	-56(%rbp), %rax
	movsd	%xmm0, (%rax)
	jmp	.L62
.L69:
	movl	-4(%rbp), %eax
	andl	$128, %eax
	testl	%eax, %eax
	je	.L71
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -48(%rbp)
	leaq	-96(%rbp), %rax
	movl	-4(%rbp), %edx
	movl	%edx, %r8d
	leaq	16(%rbp), %rdx
	movq	%rax, %rcx
	call	__scan_float
	fldt	-96(%rbp)
	movq	-48(%rbp), %rax
	fstpt	(%rax)
	jmp	.L62
.L71:
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -40(%rbp)
	leaq	-96(%rbp), %rax
	movl	-4(%rbp), %edx
	movl	%edx, %r8d
	leaq	16(%rbp), %rdx
	movq	%rax, %rcx
	call	__scan_float
	fldt	-96(%rbp)
	fstps	-104(%rbp)
	movss	-104(%rbp), %xmm0
	movq	-40(%rbp), %rax
	movss	%xmm0, (%rax)
	jmp	.L62
.L65:
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -32(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_str
	movq	-32(%rbp), %rdx
	movq	%rax, (%rdx)
	jmp	.L62
.L63:
	movq	32(%rbp), %rax
	leaq	8(%rax), %rdx
	movq	%rdx, 32(%rbp)
	movq	(%rax), %rax
	movq	%rax, -24(%rbp)
	movl	-4(%rbp), %eax
	movl	%eax, %edx
	leaq	16(%rbp), %rcx
	call	__scan_char
	movq	-24(%rbp), %rdx
	movb	%al, (%rdx)
	nop
.L62:
	addl	$1, -12(%rbp)
	jmp	.L33
.L34:
	movq	16(%rbp), %rax
	movzbl	(%rax), %edx
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	%al, %dl
	jne	.L72
	movq	16(%rbp), %rax
	addq	$1, %rax
	movq	%rax, 16(%rbp)
	addq	$1, 24(%rbp)
	jmp	.L33
.L72:
	movl	-12(%rbp), %eax
	jmp	.L53
.L33:
	addq	$1, 24(%rbp)
.L31:
	movq	24(%rbp), %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jne	.L73
	movl	-12(%rbp), %eax
.L53:
	addq	$144, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
	.def	__digit;	.scl	2;	.type	32;	.endef
	.def	__isbdigit;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	strtold;	.scl	2;	.type	32;	.endef
	.def	atoi;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
