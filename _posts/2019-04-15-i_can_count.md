---
layout: post
title: i can count
category: Reversing
source: "PlaidCTF 2019"
rpath: /resource/i_can_count
tag: []
---

**Category**: Reversing

**Source**: PlaidCTF 2019

**Points**: 50

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Let's do this together. You do know how to [count]({{site.github.master}}{{page.rpath}}/i_can_count), don't you?

## Write-up

main() 함수를 보면 decimal string 형태의 flag를 1씩 증가시키면서 입력받은 값이 flag와 동일한지 확인 후 check_flag()로 원했던 flag 값 까지 도달했는지를 확인하고 있다.

```c
[...]

  while ( 1 )
  {
    incr_flag();
    printf("> ");
    fflush(stdout);
    fgets(s, 30, stdin);
    if ( s[0] && s[strlen(s) - 1] <= 31 )
      s[strlen(s) - 1] = 0;
    if ( strcmp(s, flag_buf) )
    {
      printf("No, the correct number is %s.\n", flag_buf);
      puts("But I believe in you. Let's try again sometime!");
      exit(1);
    }
    v4 = get_compliment();
    puts(v4);
    check_flag();

[...]
```

check_flag() 함수가 핵심인 것 같다. 좀 더 들여다 보자.

```c
[...]

  for ( i = 0; ; ++i )
  {
    if ( i > 19 )
    {
      printf("PCTF{%s}\n", flag_buf);
      exit(0);
    }
    v0 = flag_buf[i];
    v1 = v0 & 3;
    v2 = (v0 >> 2) & 3;
    v3 = (v0 >> 4) & 0xF;
    LODWORD(v4) = rol(v1 + 0xA55AA55AA559LL, 2);
    v5 = v4;
    LODWORD(v6) = rol(v2 - v4 + 0xA55AA55AA559LL, 13);
    v7 = v6;
    LODWORD(v8) = rol(v3 - v6 + 0xA55AA55AA559LL, 17);
    v9 = v8;
    v10 = v7 ^ v8 ^ v5;
    LODWORD(v11) = rol((v7 & ~(v7 ^ v8 ^ v5) | v8 & (v7 ^ v8 ^ v5)) + v5 + v3 + 68453106630LL, 3);
    v12 = v11;
    LODWORD(v13) = rol((v9 & ~v11 | v10 & v11) + v7 + v1 + 68453106630LL, 11);
    v14 = v13;
    LODWORD(v15) = rol((v12 & ~v9 | v13 & v9) + v10 + v2 + 68453106630LL, 19);
    v16 = v15;
    LODWORD(v17) = rol((v14 ^ v9 ^ v15) + v12 + v2 + 201504941903014LL, 5);
    v18 = v17;
    LODWORD(v19) = rol((v16 ^ v17 ^ v14) + v9 + v1 + 201504941903014LL, 7);
    v20 = v19;
    LODWORD(v21) = rol((v18 ^ v14 ^ v19) + v16 + v3 + 201504941903014LL, 23);
    v22 = (unsigned int)((unsigned __int64)(v20 + v21 + v18 + v14) >> 32) ^ (unsigned __int64)(v20 + v21 + v18 + v14);
    v23 = (v22 >> 16) ^ v22;
    result = (unsigned __int8)(BYTE1(v23) ^ v23);
    if ( *((_BYTE *)check_buf + i) != (BYTE1(v23) ^ (unsigned __int8)v23) )
      break;
  }

[...]
```

대부분의 변수가 64bit 정수로 구성되어 있고, rol()을 이용한 계산을 거친 결과가 마지막 if문의 조건을 만족해야 한다.

```c
unsigned __int64 __cdecl rol(unsigned __int64 a1, char sh)
{
  int high; // edx
  int low; // eax
  int v4; // ebx
  __int16 v5; // si
  unsigned __int64 v6; // rax
  unsigned __int64 result; // rax

  high = a1 << sh >> 32;
  low = (_DWORD)a1 << sh;
  if ( sh & 0x20 )
  {
    high = (_DWORD)a1 << sh;
    low = 0;
  }
  v4 = low;
  v5 = high;
  v6 = a1 >> ((48 - sh) & 0x1F);
  if ( (48 - sh) & 0x20 )
  {
    LODWORD(v6) = HIDWORD(v6);
    WORD2(v6) = 0;
  }
  LODWORD(v6) = v6 | v4;
  HIDWORD(result) = (unsigned __int16)(WORD2(v6) | v5);
  return result;
}
```

rol() 함수는 rotate left 동작을 하는데, rotate left를 임의로 구현했더니 동작 결과가 조금 달라서 주어진 rol() 함수를 그대로 이용해야 했다.

IDA가 decompile 해준 check_flag() 함수와 rol() 함수를 그대로 python으로 옮겼더니 제대로 동작하지 않았다. 64bit 연산이 적용된 경우에 IDA의 decompile이 부정확한 경우가 있어서, assembly 코드를 보고 python 함수를 구현했다.([code]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **PCTF{2052419606511006177}**

이렇게 해서 풀긴 풀었는데, 풀고 나서 다시 생각해보니 flag_buf에 들어있는 값들이 복잡해 보이지만 사실 딱 10종류이다.

check_flag() 함수를 자세히 보면 flag의 각 자리수를 검사하는데, 자리수 간에 의존성이 없으니 flag_buf에 있는 10가지 숫자가 0부터 9까지의 숫자에 1:1로 대응된다.

그냥 gdb에서 1부터 10까지 넣어가면서 if문의 비교 값들을 확인해봤으면 금방 풀 수 있었을텐데 assembly 코드를 한땀한땀 보느라 너무 많은 시간을 허비했다. 다른팀들 풀이 시간을 보니 20분 정도만에 풀었던데 아마도 그렇게 푼 것 같다.
