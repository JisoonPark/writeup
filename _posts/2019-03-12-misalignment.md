---
layout: post
title: misalignment
category: Pwnable
source: "pwnable.xyz"
rpath: /resource/misalignment
tag: []
---

**Category**: Pwnable

**Source**: pwnable.xyz

**Points**: 50

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Try not using a debugger for this one.
> 
> svc.pwnable.xyz : 30003
> 
> [download]({{site.github.master}}{{page.rpath}}/challenge)

## Write-up

역시나 뭔가를 넣어야 한다. IDA로 disassemble해서 코드를 확인해보자.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [rsp+10h] [rbp-A0h]
  _QWORD v5[3]; // [rsp+18h] [rbp-98h]
  __int64 v6; // [rsp+30h] [rbp-80h]
  __int64 v7; // [rsp+38h] [rbp-78h]
  __int64 v8; // [rsp+40h] [rbp-70h]
  unsigned __int64 v9; // [rsp+A8h] [rbp-8h]

  v9 = __readfsqword(0x28u);
  setup(*(_QWORD *)&argc, argv, envp);
  memset(&s, 0, 0x98uLL);
  *(_QWORD *)((char *)v5 + 7) = 0xDEADBEEFLL;
  while ( (unsigned int)_isoc99_scanf("%ld %ld %ld", &v6, &v7, &v8) == 3 && v8 <= 9 && v8 >= -7 )
  {
    v5[v8 + 6] = v6 + v7;
    printf("Result: %ld\n", v5[v8 + 6]);
  }
  if ( *(_QWORD *)((char *)v5 + 7) == 0xB000000B5LL )
    win();
  return 0;
}
```

이 문제도 역시 세 수를 입력 받는데, arbitrary write가 가능한 구문이 존재한다.

다만, v5 배열은 QWORD로 64bit align 되어 있어서, 8의 배수인 주소값 기준으로만 접근이 가능하다.

그러므로 문제의 if문의 조건을 만족시기키 위해서는 두 번의 write가 필요하다.

little endian을 고려하였을 때, v5[0]에는 0xb500000000000000을 넣고 v5[1]에는 0x0b000000을 넣어주면 될 것 같다.

여기서 함정이 하나 있는데, 0xb500000000000000은 msb가 1이므로 음수로 넣어주어야 하는 것을 잊지 말자.

0xb500000000000000에 해당하는 -5404319552844595200과 0x0b000000에 해당하는 184549376을 넣어주면 문제를 해결할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **FLAG{u_cheater_used_a_debugger}**
