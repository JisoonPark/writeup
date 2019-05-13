#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL

void *find(void *addr, size_t siz)
{
	void *ptr = mmap(addr, siz, 1, 0x20 | 0x2, -1, 0);
	void *r;
	
	munmap(ptr, siz);

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
	r = find(addr, siz);
	if (r) return r;
	return find(addr + siz, siz); 
}

void *shellcode()
{
	size_t step = 1048576 * 64;		//64M
	void* i;
	void* r = NULL;
    printf("Hi! Soon I'll be your shellcode!\n");

    for (i = (void*)ADDR_MIN; i < (void*)(ADDR_MIN * 2); i = (void*)((unsigned long long)i + step))
    {
    	r = find(i, step);
    	if (r) return r;
    }

    if (r == NULL)
	    return (void*) 0x123456; // For this simplified test it's also OK to return the address
	return NULL;
}
