---
layout: post
title: KNOW_YOUR_MEM
category: Misc
source: "DEFCON CTF 2019 Qulas."
rpath: /resource/KNOW_YOUR_MEM
tag: [mmap]
---

**Category**: Misc

**Source**: DEFCON CTF 2019 Qulas.

**Points**: Not fixed yet

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Find the flag page in memory, 64-bit edition. Timeouts are strict, please test locally first! There's a simplified version to help with that.
> 
> know_your_mem.quals2019.oooverflow.io 4669
> 
> Files:  
> [Makefile]({{site.github.master}}{{page.rpath}}/Makefile)  
> [README.md]({{site.github.master}}{{page.rpath}}/README.md)  
> [know_your_mem.c]({{site.github.master}}{{page.rpath}}/know_your_mem.c)  
> [shellcode.c]({{site.github.master}}{{page.rpath}}/shellcode.c)  
> [simplified.c]({{site.github.master}}{{page.rpath}}/simplified.c)  
> [simplified_shellcode.so.c]({{site.github.master}}{{page.rpath}}/simplified_shellcode.so.c)  
> [topkt.py]({{site.github.master}}{{page.rpath}}/topkt.py)

## Write-up

메모리의 임의의 주소에 숨겨진 flag를 찾는 문제이다.

Makefile과 know_your_mem.c 파일을 보면 돌아가는 구조를 파악할 수 있다.

```c
#ifdef SIMPLIFIED
    shellcodefn shellcode = load_shellcode((argc >= 2) ? argv[1] : "./simplified_shellcode.so");
    //system("cat /proc/$PPID/maps");
#else
    shellcodefn shellcode = load_shellcode();
#endif


#ifdef SIMPLIFIED
    void *secret_addr =
#endif
        put_secret_somewhere_in_memory();
    put_fakes_in_memory();


    fflush(NULL);
    filter_syscalls();
    void *found = shellcode();
    fprintf(stderr, "[*] Your shellcode returned %p\n", found);

#ifdef SIMPLIFIED
    if (got_alarm)
        fprintf(stderr, "[W] Your solution took too long! Try adjusting it a bit. It should comfortably fit in the time limit.\n");
    if (secret_addr == found) {
        fprintf(stderr, "[^] Success! Make sure you're also printing the flag, and that it's not taking too long. Next: convert your solution to raw shellcode -- you can start with C code, BTW! shellcode.c shows one way to do it.\n");
        return 0;
    } else {
        fprintf(stderr, "[!] Sorry, you didn't find the secret address.\n");
        return 1;
    }
#endif
```

먼저 shell code를 읽어오고, 메모리의 임의의 주소에 flag과 fake 메세지들을 저장한 후 seccomp를 걸고 shell code를 수행하도록 하고 있다.

메세지가 저장되는 메모리 주소는 0x100000000000 번지부터 0x200000000000 번지까지 4096 byte 단위로 선택된다.

seccomp를 통해 read, write, map, munmap, mprotect 등의 system call만 수행할 수 있도록 제한되기 때문에 process의 memory map을 참조할 수는 없다.

10초의 timeout과 CPU 사용량 제한이 걸려있기 때문에 4096 byte씩 순차적으로 탐색하는 방법은 사용할 수 없으므로, 최대한 빠르게 탐색할 수 있는 방법을 생각해 보자.

문제에서 메세지를 숨기기 위해 mmap으로 메모리를 할당받아 사용하고 있고, seccomp에서도 mmap과 munmap을 사용할 수 있도록 하고 있으니 이를 이용하면 될 것 같다.

먼저, mmap의 동작을 간단하게 이해할 필요가 있는데, mmap은 할당받고 싶은 메모리 공간을 지정할 수 있으나 해당 주소에 할당이 어려운 경우에는 옵션에 따라 할당에 실패하거나 지정한 주소가 아닌 다른 주소의 메모리가 할당될 수 있다.

할당 받고자 하는 메모리 공간이 이미 사용중인 경우 재할당을 받을 수 없으니, 메모리 공간을 적당히 큰 덩어리로 나누어 mmap을 시도해 보고 mmap이 실패하는 경우에 해당 공간을 쪼개가면서 mmap 할당을 반복해보면 이미 할당된 주소들을 찾아낼 수 있을 것 같다.

우선 한번에 할당받을 수 있는 메모리의 최대 크기를 찾아보면 64MB 정도인 것을 알 수 있다. 문제에서 사용하는 메모리 공간을 64MB 단위로 나누어 위의 전략대로 탐색하는 [코드]({{site.github.master}}{{page.rpath}}/simplified_shellcode.so.solve.c)를 작성해보자.

쪼갠 크기가 4096 byte크기가 될때까지 탐색을 반복하다가 해당 메모리의 값이 "OOO:"로 시작하는지 확인해보면 제대로 찾았는지를 알 수 있다.

c 파일 버전으로 제대로 동작하는 것을 확인 했으면 이번에는 같은 내용을 shellcode로 작성해보자.

[shellcode.c]({{site.github.master}}{{page.rpath}}/shellcode.c) 파일에 가이드가 있는데, linux_syscall_support를 사용하면 linux 헤더파일과 libc 라이브러리 참조 없이 간단하게 system call을 byte code로 구현할 수 있다.

c로 구현했던 내용을 동일하게 작성하면서 mmap과 munmap 부분을 system call 호출로 변경하고 (shell code는 첫 instruction부터 수행되므로) start 함수가 먼저 호출되도록 flag를 추가해 주었다.

[작성한 코드]({{site.github.master}}{{page.rpath}}/shellcode.solve.c)를 local에서 실행한 결과 정상적으로 동작함을 확인할 수 있었고, 이를 서버에 적용하여 flag를 얻어내었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **OOO{so many bits, so many syscalls}**
