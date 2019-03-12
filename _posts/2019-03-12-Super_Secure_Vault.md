---
layout: post
title: Super Secure Vault
category: Reversing
source: "Pragyan CTF 19"
rpath: /resource/Super_Secure_Vault
tag: [CRT]
---

**Category**: Reversing/Binary

**Source**: Pragyan CTF 19

**Points**: 400

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Open the Vault to get the treasure.
> 
> [vault]({{site.github.master}}{{page.rpath}}/vault)

## Write-up

main() 함수를 보면 먼저 key를 입력받아서 몇가지 조건을 검사한다.

```c
[...]

  v13 = 8;
  v14 = 229;
  v15 = 5;
  v16 = 25;
  v17 = 4;
  v18 = 83;
  v19 = 7;
  v20 = 135;
  v21 = 5;
  printf("Enter the key: ", argv, envp);
  __isoc99_scanf("%s", &s);
  if ( strlen(&s) > 0x1E )
    fail(0LL);
  v3 = getNum((__int64)"27644437104591489104652716127", 0, v13);
  if ( (unsigned int)mod(&s, v3) != v12 )
    fail(0LL);
  v9 = v13;
  v4 = getNum((__int64)"27644437104591489104652716127", v13, v15);
  if ( (unsigned int)mod(&s, v4) != v14 )
    fail(0LL);
  v10 = v15 + v9;
  v5 = getNum((__int64)"27644437104591489104652716127", v10, v17);
  if ( (unsigned int)mod(&s, v5) != v16 )
    fail(0LL);
  v11 = v17 + v10;
  v6 = getNum((__int64)"27644437104591489104652716127", v11, v19);
  if ( (unsigned int)mod(&s, v6) != v18 )
    fail(0LL);
  v8 = getNum((__int64)"27644437104591489104652716127", v19 + v11, v21);
  if ( (unsigned int)mod(&s, v8) != v20 )
    fail(0LL);
  printf("Enter password: ", v8);
  __isoc99_scanf("%s", &v23);
  func2((__int64)&v23, &s, "27644437104591489104652716127");

[...]
```

getNum(n, index, len) 함수는 문자열 형태로 주어진 십진수 숫자 n에서, index부터 len 만큼을 정수형으로 읽어오는 함수이다.

mod(n, d) 함수는 문자열 형태로 주어진 십진수 숫자를 d로 나눈 나머지를 돌려주는 함수이다.

즉, 5번의 if문은 입력 key에 대해, 아래와 같이 key % d = r 형태의 방정식 5개를 정의하고 있다.

```
key % 27644437 = 213
key % 10459 = 229
key % 1489 = 25
key % 1046527 = 83
key % 16127 = 135
```

이 5개의 방정식을 모두 만족시키는 key는 CRT(Chinese Remainder Theorem)을 이용하면 구할 수 있다.

[여기](https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_2.7)에 python으로 구현된 CRT가 있어서 가져다 사용했다.

CRT를 풀면 **3087629750608333480917556**라는 key를 얻을 수 있다.

key를 입력하고 나면 이번엔 password를 입력받아서 func2() 함수로 들어간다.

```c
int __fastcall func2(__int64 a1, char *a2, const char *a3)
{

[...]

  v12 = strcat(a2, a3);
  v3 = (unsigned __int64)&v12[strlen(v12)];
  *(_WORD *)v3 = 0x3038;
  *(_BYTE *)(v3 + 2) = 0;
  v7 = 0;
  v8 = 0;
  v10 = strlen(v12) >> 1;
  while ( v8 < strlen(v12) >> 1 )
  {
    if ( *(_BYTE *)(v7 + a1) != matrix[100 * (10 * (v12[v8] - 48) + v12[v8 + 1] - 48)
                                     - 48
                                     + 10 * (v12[v10] - 48)
                                     + v12[v10 + 1]] )
      fail(1LL);
    ++v7;
    v8 += 2;
    v10 += 2;
  }
  v9 = 0;
  v11 = strlen(v12) >> 1;
  while ( v9 < strlen(v12) >> 1 )
  {
    v4 = 10 * (v12[v9] - 48) + v12[v9 + 1] - 48;
    v5 = 10 * (v12[v11] - 48) + v12[v11 + 1] - 48;
    if ( *(_BYTE *)(v7 + a1) != matrix[100 * (v4 * v4 % 97) + v5 * v5 % 97] )
      fail(1LL);
    ++v7;
    v9 += 2;
    v11 += 2;
  }
  puts("Your Skills are really great. Flag is:");
  return printf("pctf{\%s}\n", a1);
}
```

password로 입력받은 값이 matrix배열의 특정 위치의 값들과 동일한지 검사하는 루틴이다.

자세히 보면 v7을 1씩 증가시키면서 password의 앞에서부터 한 글자씩 비교하는 것을 볼 수 있는데, 이 비교 구문을 그냥 순서대로 쭉 모으면 password로 어떤 값을 넣어야 하는지 알 수 있다.

알고리즘들이 porting 하기에 비교적 간단해서 그냥 python으로 동일한 [프로그램]({{site.github.master}}{{page.rpath}}/ex.py)을 구현하여 실행한 결과, password를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **pctf{R3v3rS1Ng_#s_h311_L0t_Of_Fun}**
