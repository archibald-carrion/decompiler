	.file	"100092.c"
	.text
	.globl	consumer_c
	.def	consumer_c;	.scl	2;	.type	32;	.endef
	.seh_proc	consumer_c
consumer_c:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	.seh_endprologue
	nop
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
