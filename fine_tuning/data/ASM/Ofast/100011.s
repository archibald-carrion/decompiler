	.file	"100011.c"
	.text
	.p2align 4
	.def	__scan_uint;	.scl	3;	.type	32;	.endef
	.seh_proc	__scan_uint
__scan_uint:
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
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	(%rcx), %rax
	movq	%rcx, %rsi
	movl	%edx, %edi
	movsbl	(%rax), %ecx
	testb	$1, %r8b
	jne	.L7
	testb	$2, %r8b
	je	.L15
	movl	$16, %r12d
	movl	$16, %ebp
.L2:
	xorl	%ebx, %ebx
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L6:
	movq	(%rsi), %rax
	imull	%r12d, %ebx
	movl	%ebp, %edx
	movsbl	(%rax), %ecx
	call	__digit
	addl	%eax, %ebx
	movq	(%rsi), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, (%rsi)
	subl	$1, %edi
	je	.L1
	movsbl	1(%rax), %ecx
.L4:
	movl	%ebp, %edx
	call	__isbdigit
	testl	%eax, %eax
	jne	.L6
.L1:
	movl	%ebx, %eax
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	movl	$10, %r12d
	movl	$10, %ebp
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L15:
	andl	$4, %r8d
	je	.L16
	movl	$8, %r12d
	movl	$8, %ebp
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L16:
	movl	$10, %r12d
	movl	$10, %ebp
	cmpb	$48, %cl
	jne	.L2
	leaq	1(%rax), %rdx
	movq	%rdx, (%rsi)
	movsbl	1(%rax), %ecx
	movl	%ecx, %edx
	andl	$-33, %edx
	cmpb	$88, %dl
	je	.L3
	subl	$1, %edi
	movl	$8, %r12d
	movl	$8, %ebp
	jmp	.L2
.L3:
	leaq	2(%rax), %rdx
	subl	$2, %edi
	movl	$16, %r12d
	movl	$16, %ebp
	movq	%rdx, (%rsi)
	movsbl	2(%rax), %ecx
	jmp	.L2
	.seh_endproc
	.p2align 4
	.globl	vsscanf
	.def	vsscanf;	.scl	2;	.type	32;	.endef
	.seh_proc	vsscanf
vsscanf:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
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
	subq	$120, %rsp
	.seh_stackalloc	120
	.seh_endprologue
	movzbl	(%rdx), %eax
	movq	%rcx, 192(%rsp)
	movq	%rdx, %rsi
	movq	%r8, 208(%rsp)
	movl	$0, 44(%rsp)
	testb	%al, %al
	je	.L17
	movq	__imp_isspace(%rip), %rdi
	jmp	.L70
	.p2align 4,,10
	.p2align 3
.L23:
	movq	192(%rsp), %rdx
	cmpb	%al, (%rdx)
	jne	.L17
	addq	$1, %rdx
	leaq	1(%rsi), %rbx
	movq	%rdx, 192(%rsp)
.L22:
	movzbl	1(%rbx), %eax
	leaq	1(%rbx), %rsi
	testb	%al, %al
	je	.L17
.L70:
	movq	192(%rsp), %rbx
	cmpb	$32, %al
	je	.L20
	cmpb	$37, %al
	jne	.L23
	movzbl	1(%rsi), %eax
	cmpb	$42, %al
	je	.L24
	movsbl	%al, %ecx
	leaq	1(%rsi), %rbx
	movl	$130, 72(%rsp)
	movl	$66, %r10d
	subl	$48, %ecx
	movl	$146, 68(%rsp)
	movl	$82, %r9d
	movl	$68, %r11d
	movl	$132, 64(%rsp)
	movl	$65, %r8d
	xorl	%esi, %esi
	movl	$2, %edx
	movl	$129, 56(%rsp)
	movl	$18, %r15d
	movl	$4, %r13d
	movl	$1, %r14d
	movl	$128, 48(%rsp)
	movl	$64, %r12d
	movl	$-1, %ebp
	cmpl	$9, %ecx
	jbe	.L92
.L26:
	cmpb	$108, %al
	je	.L93
	movl	%esi, %r12d
	cmpb	$76, %al
	jne	.L29
	movl	72(%rsp), %edx
	movl	68(%rsp), %r15d
	addq	$1, %rbx
	movzbl	(%rbx), %eax
	movl	56(%rsp), %r14d
	movl	64(%rsp), %r13d
	movl	48(%rsp), %r12d
.L29:
	subl	$88, %eax
	cmpb	$32, %al
	ja	.L17
	leaq	.L32(%rip), %rcx
	movzbl	%al, %eax
	movslq	(%rcx,%rax,4), %rax
	addq	%rcx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L32:
	.long	.L76-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L38-.L32
	.long	.L37-.L32
	.long	.L17-.L32
	.long	.L36-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L35-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L34-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L33-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L17-.L32
	.long	.L31-.L32
	.text
	.p2align 4,,10
	.p2align 3
.L21:
	movq	%rbx, 192(%rsp)
.L20:
	movsbl	(%rbx), %ecx
	addq	$1, %rbx
	call	*%rdi
	testl	%eax, %eax
	jne	.L21
	movq	%rsi, %rbx
	movzbl	1(%rbx), %eax
	leaq	1(%rbx), %rsi
	testb	%al, %al
	jne	.L70
.L17:
	movl	44(%rsp), %eax
	addq	$120, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
.L76:
	movl	%r15d, %r13d
.L34:
	testl	%esi, %esi
	je	.L94
	movl	%r13d, %r8d
	movl	%ebp, %edx
	leaq	192(%rsp), %rcx
	call	__scan_uint
	.p2align 4,,10
	.p2align 3
.L53:
	addl	$1, 44(%rsp)
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L93:
	movzbl	1(%rbx), %eax
	movl	%r10d, %edx
	movl	%r9d, %r15d
	movl	%r8d, %r14d
	movl	%r11d, %r13d
	addq	$1, %rbx
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L24:
	movzbl	2(%rsi), %eax
	leaq	2(%rsi), %rbx
	movl	$162, 72(%rsp)
	movl	$98, %r10d
	movl	$178, 68(%rsp)
	movl	$114, %r9d
	movl	$100, %r11d
	movl	$97, %r8d
	movsbl	%al, %ecx
	movl	$164, 64(%rsp)
	movl	$34, %edx
	movl	$50, %r15d
	subl	$48, %ecx
	movl	$161, 56(%rsp)
	movl	$36, %r13d
	movl	$33, %r14d
	movl	$96, %r12d
	movl	$32, %esi
	movl	$-1, %ebp
	movl	$160, 48(%rsp)
	cmpl	$9, %ecx
	ja	.L26
.L92:
	movq	%rbx, %rcx
	movl	%r10d, 92(%rsp)
	movl	%r9d, 88(%rsp)
	movl	%r11d, 84(%rsp)
	movl	%r8d, 80(%rsp)
	movl	%edx, 76(%rsp)
	call	atoi
	movsbl	(%rbx), %ecx
	movl	76(%rsp), %edx
	movl	%eax, %ebp
	movl	80(%rsp), %r8d
	movl	84(%rsp), %r11d
	movl	%ecx, %eax
	subl	$48, %ecx
	movl	88(%rsp), %r9d
	movl	92(%rsp), %r10d
	cmpl	$9, %ecx
	ja	.L26
	.p2align 4,,10
	.p2align 3
.L27:
	movsbl	1(%rbx), %ecx
	addq	$1, %rbx
	movl	%ecx, %eax
	subl	$48, %ecx
	cmpl	$9, %ecx
	jbe	.L27
	jmp	.L26
.L33:
	testl	%esi, %esi
	je	.L48
	testl	%ebp, %ebp
	jle	.L95
	movq	192(%rsp), %rsi
	movq	__imp_isspace(%rip), %r12
	xorl	%r13d, %r13d
	movq	%rsi, %r14
	jmp	.L55
	.p2align 4,,10
	.p2align 3
.L97:
	testl	%eax, %eax
	jne	.L54
	addq	$1, %r14
	cmpl	%r13d, %ebp
	je	.L96
.L55:
	movsbl	(%r14), %ecx
	movl	%ecx, %r15d
	call	*%r12
	movl	%r13d, %edx
	leal	1(%r13), %r13d
	testb	%r15b, %r15b
	jne	.L97
.L54:
	leal	1(%rdx), %ecx
	movl	%edx, 48(%rsp)
	movslq	%ecx, %rcx
	call	malloc
	movslq	48(%rsp), %rdx
	testl	%edx, %edx
	je	.L79
.L71:
	movq	%rax, %rcx
	leaq	(%rsi,%rdx), %r9
	.p2align 4,,10
	.p2align 3
.L58:
	movzbl	(%rsi), %r8d
	addq	$1, %rsi
	addq	$1, %rcx
	movq	%rsi, 192(%rsp)
	movb	%r8b, -1(%rcx)
	cmpq	%r9, %rsi
	jne	.L58
	addq	%rax, %rdx
.L57:
	movb	$0, (%rdx)
	movq	%rax, %rcx
	call	free
	jmp	.L53
	.p2align 4,,10
	.p2align 3
.L48:
	movq	208(%rsp), %rax
	addq	$8, %rax
	movq	%rax, 48(%rsp)
	movq	208(%rsp), %rax
	movq	(%rax), %r14
	testl	%ebp, %ebp
	jle	.L64
	movq	__imp_isspace(%rip), %r12
	movq	192(%rsp), %r15
	movq	%rbx, 56(%rsp)
	movq	%r12, %r13
	movq	%r15, %rbx
	movl	%esi, %r12d
	jmp	.L66
	.p2align 4,,10
	.p2align 3
.L99:
	testb	%sil, %sil
	je	.L65
	addq	$1, %rbx
	cmpl	%r12d, %ebp
	je	.L98
.L66:
	movsbl	(%rbx), %ecx
	movl	%ecx, %esi
	call	*%r13
	movl	%r12d, %r8d
	leal	1(%r12), %r12d
	testl	%eax, %eax
	je	.L99
.L65:
	leal	1(%r8), %ecx
	movq	56(%rsp), %rbx
	movl	%r8d, 56(%rsp)
	movslq	%ecx, %rcx
	call	malloc
	movslq	56(%rsp), %r8
	testl	%r8d, %r8d
	je	.L80
.L72:
	movq	%rax, %rdx
	leaq	(%r15,%r8), %r9
	.p2align 4,,10
	.p2align 3
.L69:
	movzbl	(%r15), %ecx
	addq	$1, %r15
	addq	$1, %rdx
	movq	%r15, 192(%rsp)
	movb	%cl, -1(%rdx)
	cmpq	%r9, %r15
	jne	.L69
	addq	%rax, %r8
.L68:
	movb	$0, (%r8)
	movq	%rax, (%r14)
	movq	48(%rsp), %rax
	movq	%rax, 208(%rsp)
	jmp	.L53
.L35:
	testl	%esi, %esi
	je	.L78
	movq	192(%rsp), %rax
	leal	-1(%rbp), %edx
	cmpb	$45, (%rax)
	je	.L100
.L51:
	movl	%r12d, %r8d
	leaq	192(%rsp), %rcx
	call	__scan_uint
	jmp	.L53
.L36:
	movq	192(%rsp), %rdx
	testl	%esi, %esi
	je	.L101
	leaq	96(%rsp), %rcx
	leaq	192(%rsp), %r8
	call	strtold
	jmp	.L53
	.p2align 4,,10
	.p2align 3
.L101:
	movq	208(%rsp), %rax
	leaq	96(%rsp), %rcx
	leaq	192(%rsp), %r8
	movq	(%rax), %rsi
	testb	$64, %r12b
	jne	.L102
	andl	$128, %r12d
	je	.L63
	call	strtold
	fldt	96(%rsp)
	fstpt	(%rsi)
.L62:
	addq	$8, 208(%rsp)
	jmp	.L53
.L37:
	testl	%esi, %esi
	je	.L41
	movq	192(%rsp), %rax
	movl	%r14d, %r12d
	leal	-1(%rbp), %edx
	cmpb	$45, (%rax)
	jne	.L51
	jmp	.L100
	.p2align 4,,10
	.p2align 3
.L78:
	movl	%r12d, %r14d
.L41:
	movq	208(%rsp), %rax
	leal	-1(%rbp), %edx
	movq	(%rax), %r12
	leaq	8(%rax), %rsi
	movq	192(%rsp), %rax
	cmpb	$45, (%rax)
	je	.L103
	movl	%r14d, %r8d
	leaq	192(%rsp), %rcx
	call	__scan_uint
.L60:
	movl	%eax, (%r12)
	movq	%rsi, 208(%rsp)
	jmp	.L53
.L38:
	movq	192(%rsp), %rax
	leaq	1(%rax), %rdx
	testl	%esi, %esi
	je	.L104
	movq	%rdx, 192(%rsp)
	jmp	.L53
	.p2align 4,,10
	.p2align 3
.L104:
	movq	208(%rsp), %rsi
	movzbl	(%rax), %eax
	movq	%rdx, 192(%rsp)
	movq	(%rsi), %rcx
	movb	%al, (%rcx)
	movq	%rsi, %rax
	addq	$8, %rax
	movq	%rax, 208(%rsp)
	jmp	.L53
	.p2align 4,,10
	.p2align 3
.L94:
	movq	208(%rsp), %rax
	movl	%r13d, %r8d
	movl	%ebp, %edx
	leaq	192(%rsp), %rcx
	movq	(%rax), %r12
	leaq	8(%rax), %rsi
	call	__scan_uint
	movl	%eax, (%r12)
	movq	%rsi, 208(%rsp)
	jmp	.L53
.L31:
	movl	%edx, %r13d
	jmp	.L34
.L100:
	addq	$1, %rax
	movl	%r12d, %r8d
	leaq	192(%rsp), %rcx
	movq	%rax, 192(%rsp)
	call	__scan_uint
	jmp	.L53
.L103:
	addq	$1, %rax
	movl	%r14d, %r8d
	leaq	192(%rsp), %rcx
	movq	%rax, 192(%rsp)
	call	__scan_uint
	negl	%eax
	jmp	.L60
.L102:
	call	strtold
	fldt	96(%rsp)
	fstpl	(%rsi)
	jmp	.L62
.L63:
	call	strtold
	fldt	96(%rsp)
	fstps	(%rsi)
	jmp	.L62
.L96:
	addl	$2, %edx
	movslq	%edx, %rcx
	call	malloc
	movslq	%ebp, %rdx
	jmp	.L71
.L98:
	leal	2(%r8), %ecx
	movq	56(%rsp), %rbx
	movslq	%ecx, %rcx
	call	malloc
	movslq	%ebp, %r8
	jmp	.L72
.L79:
	movq	%rax, %rdx
	jmp	.L57
.L80:
	movq	%rax, %r8
	jmp	.L68
.L64:
	movl	$1, %ecx
	call	malloc
	movq	%rax, %r8
	jmp	.L68
.L95:
	movl	$1, %ecx
	call	malloc
	movq	%rax, %rdx
	jmp	.L57
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
	.def	__digit;	.scl	2;	.type	32;	.endef
	.def	__isbdigit;	.scl	2;	.type	32;	.endef
	.def	atoi;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	strtold;	.scl	2;	.type	32;	.endef
