---
layout: post
title: Elementary
category: Reversing
source: "CONFidence CTF 2019 Teaser"
rpath: /resource/Elementary
tag: [angr, idapython]
---

**Category**: Reversing

**Source**: CONFidence CTF 2019 Teaser

**Points**: ???

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Elementary, my dear Watson.
> 
> [elementary.tar.gz]({{site.github.master}}{{page.rpath}}/elementary.tar.gz)

## Write-up

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [rsp+0h] [rbp-90h]
  unsigned __int64 v5; // [rsp+88h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  printf("Password: ", argv, envp);
  __isoc99_scanf("%s", &v4);
  if ( (unsigned int)checkFlag(&v4) )
    printf("Good job!", &v4);
  else
    printf("Wrong!", &v4);
  return 0;
}
```

Password를 입력 받는데, 특정 조건을 만족하는 Password 자체가 flag인 전형적인 angr 문제이다.

```c
_BOOL8 __fastcall checkFlag(char *a1)
{
  if ( (unsigned int)function0(a1[64] & 1) )
    return 0LL;
  if ( (unsigned int)function1((a1[64] >> 2) & 1) )
    return 0LL;
  if ( (unsigned int)function2((a1[64] >> 5) & 1) )
    return 0LL;
  if ( (unsigned int)function3((a1[64] >> 4) & 1) )
    return 0LL;

[...]
```

checkFlag() 함수는 function0() 부터 function831() 까지의 함수를 이용해서 Password를 체크한다.

더 볼것도 없이 angr를 이용해서 password를 찾아보자.

```python
import angr
succ_addr = 0x40077f
fail_addr = 0x400792

proj = angr.Project('./elementary', load_options={"auto_load_libs": False})

sm = proj.factory.simulation_manager()
sm.explore(find = (succ_addr,), avoid = (fail_addr,))

if len(sm.found) < 1:
    print "not found!"
else:
    s = sm.found[0].state.posix.dumps(0)
    print "found : " + s
```

위와 같이 exploit을 작성하여 실행해 보았으나, angr는 path 탐색에 실패했다. 이래저래 다르게 구현해봤는데 안되는걸 보니, 나중에 다른사람들 writeup을 좀 찾아봐야 할것 같다.

각각의 [function]({{site.github.master}}{{page.rpath}}/func0.txt)이 400개가 넘는 instruction으로 구성되어 있는걸 보면 각각의 함수가 좀 복잡해서 그럴 수도 있을 것 같다. 하지만 IDA에서 decompile 해보면 argument를 그대로 리턴하거나 1과 xor하여 리턴하거나 둘 중의 하나이다.

![img]({{page.rpath|prepend:site.baseurl}}/func0.png)

바이너리를 분석하기 어렵게 일부러 꼬아둔 것 같으니, IDApython을 이용해서 [checkFlag]({{site.github.master}}{{page.rpath}}/checkFlag) 함수와 각각의 functionX 함수들의 decompile한 [결과]({{site.github.master}}{{page.rpath}}/functions)를 파일로 저장하였다.

![img]({{page.rpath|prepend:site.baseurl}}/idapython.png)

checkFlag() 함수의 구성 자체는 별다른 예외 없이 일률적으로, if문 하나가 functionX 함수 하나를 이용해서 Password의 한 bit를 확인하는 식이다.

python을 이용해서 조건을 만족시기는 문자열을 찾는 [코드]({{site.github.master}}{{page.rpath}}/ex.py)를 작성하여 flag를 찾을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **p4{I_really_hope_you_automated_this_somehow_otherwise_it_might_be_a_bit_frustrating_to_do_this_manually}**
