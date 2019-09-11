---
layout: post
title: Not So Easy B0f
category: Pwnable
source: "HackCON CTF 2019"
rpath: /resource/Not_So_Easy_B0f
tag: [bof, fsb]
---

**Category**: Pwnable

**Source**: HackCON CTF 2019

**Points**: 469

**Author**: Jisoon Park(js00n.park)

**Description:** 

> I have stack canaries enabled, Can you still B0f me ? Service : nc 68.183.158.95 8991

> Download: [q3]({{site.github.master}}{{page.rpath}}/q3) [libc.so.6]({{site.github.master}}{{page.rpath}}/libc.so.6)

## Write-up

주어진 파일을 IDA로 디컴파일 해보자.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  FILE *stream; // ST08_8
  char s[8]; // [rsp+10h] [rbp-20h]
  __int64 v6; // [rsp+18h] [rbp-18h]
  unsigned __int64 v7; // [rsp+28h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  *(_QWORD *)s = 0LL;
  v6 = 0LL;
  stream = (FILE *)_bss_start;
  printf("Enter name : ", argv, envp);
  fgets(s, 16, stream);
  puts("Hello");
  printf(s, 16LL);
  printf("Enter sentence : ");
  fgets(s, 256, stream);
  return 0;
}
```

fgets()를 이용해서 두 번의 입력을 줄 수 있는데, 첫 번째 fgets()를 사용하면 fsb 공격이 가능하고, 두 번째 fgets()에서는 bof 공격이 가능하다.

libc를 줬으니 ROP 또는 Oneshot-gadget을 이용하면 될 것 같은데, 이를 위해서는 libc_base 주소를 알아내야 한다.

추가로, cananry가 적용되어 있으니 canary의 값도 겸사겸사 알아내 보자.

첫 번째 입력으로 **%11$lx:%13$lx** 을 던져주면 canary와 main 함수의 return address를 알아낼 수 있다.

main 함수는 libc.so의 \__libc_start_main에 있는 main 함수 호출 주소 다음으로 복귀하도록 되어 있으니 이를 이용하여 libc_base의 주소를 계산해낼 수 있다.

주어진 libc.so를 분석해보면 main 함수가 0x20830 offset으로 리턴될 것을 알 수 있고, oneshot gadget은 0x45216 offset에 있는 것도 알아낼 수 있다.

oneshot gadget을 이용하기 위한 재료들이 다 갖추어 졌으니 실제 libc 주소를 알아내서 bof 공격을 시도하면 shell을 얻을 수 있다. ([코드]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **d4rk{H3ll0_R0p}c0de**
