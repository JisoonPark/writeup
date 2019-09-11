---
layout: post
title: Easy Crack Me
category: Reversing
source: "TokyoWesterns CTF 5th 2019"
rpath: /resource/Easy_Crack_Me
tag: []
---

**Category**: Reversing

**Source**: TokyoWesterns CTF 5th 2019

**Points**: 94

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Cracking is easy for you.
> 
> [easy_crack_me]({{site.github.master}}{{page.rpath}}/easy_crack_me)

## Write-up

바이너리 하나를 던져주는데, 간단히 실행해보면 incorret라는 메세지를 던져준다. correct한 값을 찾으면 될 것 같다.

바이너리를 decompile 해보면 커다란 main 함수가 존재하는데 그 안에서 여러가지 체크를 하고 있다. 하나씩 알아보자.

```c
if ( strlen(a2[1]) != 39 )
{
  puts("incorrect");
  exit(0);
}
if ( memcmp(s, "TWCTF{", 6uLL) || s[38] != 125 )
{
  puts("incorrect");
  exit(0);
}
```

입력값의 길이와 flag 형식에 맞는지를 검사하는 부분이다. flalg format 부분을 제외하면 총 32글자임을 알 수 있다.

```c
v46 = '76543210';
v47 = 'fedcba98';
for ( i = 0; i <= 15; ++i )
{
  for ( j = strchr(s, *((char *)&v46 + i)); j; j = strchr(j + 1, *((char *)&v46 + i)) )
    ++*((_DWORD *)&s1 + i);
}
if ( memcmp(&s1, &unk_400F00, 0x40uLL) )
{
  puts("incorrect");
  exit(0);
}
```

hex 표현에 맞는 문자가 각각 몇 개씩 있는지 확인하는 부분이다. 0x400f00 번지에 있는 메모리를 확인해보면 모두 합쳐서 32글자임을 알 수 있다. flag가 hex digit으로만 구성되어 있나보다.

```c
v21 = 0LL;
v22 = 0LL;
v23 = 0LL;
v24 = 0LL;
v25 = 0LL;
v26 = 0LL;
v27 = 0LL;
v28 = 0LL;
for ( k = 0; k <= 7; ++k )
{
  v10 = 0;
  v11 = 0;
  for ( l = 0; l <= 3; ++l )
  {
    v5 = s[4 * k + 6 + l];
    v10 += v5;
    v11 ^= v5;
  }
  *((_DWORD *)&v21 + k) = v10;
  *((_DWORD *)&v25 + k) = v11;
}
v29 = 0LL;
v30 = 0LL;
v31 = 0LL;
v32 = 0LL;
v33 = 0LL;
v34 = 0LL;
v35 = 0LL;
v36 = 0LL;
for ( m = 0; m <= 7; ++m )
{
  v14 = 0;
  v15 = 0;
  for ( n = 0; n <= 3; ++n )
  {
    v6 = s[8 * n + 6 + m];
    v14 += v6;
    v15 ^= v6;
  }
  *((_DWORD *)&v29 + m) = v14;
  *((_DWORD *)&v33 + m) = v15;
}
if ( memcmp(&v21, &unk_400F40, 0x20uLL) || memcmp(&v25, &unk_400F60, 0x20uLL) )
{
  puts("incorrect");
  exit(0);
}
if ( memcmp(&v29, &unk_400FA0, 0x20uLL) || memcmp(&v33, &unk_400F80, 0x20uLL) )
{
  puts("incorrect");
  exit(0);
}
```

여기서는 두 가지를 확인하는데, 4바이트씩 그룹을 만들어서 각 그룹 안의 byte 값을을 더한 결과와 xor한 결과를 미리 정의된 값과 동일한지 확인하는 과정과 8 byte씩 건너뛰면서 4 byte를 모아 그 값들을 더한 결과와 xor한 결과를 또다른 미리 정의된 값과 동일한지 확인하는 과정이다.

```c
memset(v45, 0, sizeof(v45));
for ( ii = 0; ii <= 31; ++ii )
{
  v7 = s[ii + 6];
  if ( v7 <= 47 || v7 > 57 )
  {
    if ( v7 <= 96 || v7 > 102 )
      v45[ii] = 0;
    else
      v45[ii] = 128;
  }
  else
  {
    v45[ii] = 255;
  }
}
if ( memcmp(v45, &unk_400FC0, 0x80uLL) )
{
  puts("incorrect");
  exit(0);
}
```

32 byte 각 글자가 a\~f 중의 하나인지, 아니면 0\~9 중의 하나인지 확인하는 부분이다. 0x400fc0에 존재하는 array를 통해 flag의 각 글자가 숫자인지 문자인지 확인할 수 있다. 숫자 또는 a\~f 중 하나의 문자가 아닌 경우 0이 되도록 하고 있는데, 0x400fc0 번지의 array를 확인해보면 역시나 0은 없다.

```c
v18 = 0;
for ( jj = 0; jj <= 15; ++jj )
  v18 += s[2 * (jj + 3)];
if ( v18 != 1160 )
{
  puts("incorrect");
  exit(0);
}
```

flag의 짝수번째 문자들의 합이 1160인지 확인하는 부분이다.

```c
if ( s[37] != 53 || s[7] != 102 || s[11] != 56 || s[12] != 55 || s[23] != 50 || s[31] != 52 )
{
  puts("incorrect");
  exit(0);
}
printf("Correct: %s\n", s, a2);
```

flag 중의 6글자를 직접적으로 알려주는 부분이다. 여기까지의 checkf를 지나면 Correct라는 메세지를 출력한다.

위의 조건들을 모두 만족시키는 입력값을 찾아보자. 처음에는 자세히 보지 않고 angr를 이용해 보려고 했는데 한참이 지나도 적절한 입력값을 찾지 못해서 직접 decompile하여 위의 내용을 확인하고 코딩을 시도했다. ㅜㅠ ([코드]({{site.github.master}}{{page.rpath}}/ex.py))

코딩을 하다가 뭔가 조건을 빼먹었는지, 조건에 맞는 값이 800여 개 정도 찾아졌는데, 몇개 안되는 정도라 실제로 실행시켜보고 correct가 출력되는 값을 찾았다. ([코드]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **TWCTF{df2b4877e71bd91c02f8ef6004b584a5}**
