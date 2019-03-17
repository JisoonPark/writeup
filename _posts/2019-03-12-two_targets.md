---
layout: post
title: two targets
category: Pwnable
source: "pwnable.xyz"
rpath: /resource/two_targets
tag: []
---

**Category**: Pwnable

**Source**: pwnable.xyz

**Points**: 50

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Which one would you exploit?
> 
> svc.pwnable.xyz : 30031
> 
> [download]({{site.github.master}}{{page.rpath}}/challenge)

## Write-up

![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

주어진 파일을 실행시켜보면 이름, 국적, 나이를 설정하거나 shell을 얻을 수 있는 메뉴가 주어진다.  shell 메뉴를 선택해 보았지만 역시나 아무것도 실행되지 않는다.

일단 main() 함수부터 disassemble 해보자.

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  char *v3; // rsi
  int choice; // eax
  char s; // [rsp+10h] [rbp-40h]
  __int64 v6; // [rsp+30h] [rbp-20h]
  char *v7; // [rsp+40h] [rbp-10h]
  unsigned __int64 v8; // [rsp+48h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  setup(*(_QWORD *)&argc, argv, envp);
  v3 = 0LL;
  memset(&s, 0, 0x38uLL);
  while ( 1 )
  {
    while ( 1 )
    {
      print_menu();
      choice = read_int32();
      if ( choice != 2 )
        break;
      printf("nationality: ", v3);
      v3 = (char *)&v6;
      __isoc99_scanf("%24s", &v6);
    }
    if ( choice > 2 )
    {
      if ( choice == 3 )
      {
        printf("age: ", v3);
        v3 = v7;
        __isoc99_scanf("%d", v7);
      }
      else if ( choice == 4 )
      {
        if ( (unsigned __int8)auth((__int64)&s) )
          win(&s);
      }
      else
      {
LABEL_14:
        puts("Invalid");
      }
    }
    else
    {
      if ( choice != 1 )
        goto LABEL_14;
      printf("name: ", v3);
      v3 = &s;
      __isoc99_scanf("%32s", &s);
    }
  }
}
```

4번 shell 메뉴 선택 시 flag를 보여주는 win() 함수 실행 전에 현재 설정된 이름(s 변수)을 입력으로 받는 auth()라는 함수를 먼저 통과해야 한다. auth() 함수를 살펴보자.

```c
_BOOL8 __fastcall auth(__int64 a1)
{
  signed int i; // [rsp+18h] [rbp-38h]
  char s1[8]; // [rsp+20h] [rbp-30h]
  __int64 v4; // [rsp+28h] [rbp-28h]
  __int64 v5; // [rsp+30h] [rbp-20h]
  __int64 v6; // [rsp+38h] [rbp-18h]
  unsigned __int64 v7; // [rsp+48h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  *(_QWORD *)s1 = 0LL;
  v4 = 0LL;
  v5 = 0LL;
  v6 = 0LL;
  for ( i = 0; (unsigned int)i <= 0x1F; ++i )
    s1[i] = ((*(_BYTE *)(a1 + i) >> 4) | 16 * *(_BYTE *)(a1 + i)) ^ *((_BYTE *)main + i);
  return strncmp(s1, &s2, 0x20uLL) == 0;
}
```

0x20번의 loop을 돌면서 s1을 채우고, s2와 같은지 비교하는 함수이다. 살펴보면 a1의 각 byte의 상위 4bit와 하위 4bit을 뒤집고, main 함수의 byte code와 xor 하여 s1을 계산하는 것 같다.

s2는 0x401d28 번지에 문자열 상수로 선언되어 있고, main 함수의 byte code는 text 영역에서 확인할 수 있다. s2와 main 함수의 byte code를 알 수 있으니 역산해서 a1을 구하는 [코드]({{site.github.master}}{{page.rpath}}/ex.py)를 작성하여 실행하면 auth를 통과하고 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **FLAG{now_try_the_2nd_solution}**

~~flag를 얻었으니 다른 취약점에는 관심 없다~~
