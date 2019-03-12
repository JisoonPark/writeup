---
layout: post
title: Decode This
category: Crypto
source: "Pragyan CTF 19"
rpath: /resource/Decode_This
tag: [brute_force, algebra]
---

**Category**: Crypto

**Source**: Pragyan CTF 19

**Points**: 200

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Ram has something to show you, which can be of great help. It definitely contains the piece of text "pctf" and whatever follows it is the flag. Can you figure out what it is?
> 
> Note: Enclose it in pctf{}
> 
> [ciphertext.txt]({{site.github.master}}{{page.rpath}}/ciphertext.txt)  
> [encrypt.py]({{site.github.master}}{{page.rpath}}/encrypt.py)

## Write-up

먼저 encrypt.py 파일을 살펴보자.

```python
[...]

flag = ""
for i in secret:
    if i.isalpha():
        flag += i
l = len(flag)

key = [[int(random.random()*10000) for e in range(2)] for e in range(2)]

i = 0
ciphertext = ""

while i <= (l-2):
    x = ord(flag[i]) - 97
    y = ord(flag[i+1]) - 97
    z = (x*key[0][0] + y*key[0][1])%26 + 97
    w = (x*key[1][0] + y*key[1][1])%26 + 97
    ciphertext = ciphertext + chr(z) + chr(w)
    i = i+2

[...]
```

key list에 있는 4가지 key 값을 찾아야 한다. 각각의 key 값은 (0, 10000) 범위에 있어서, 얼핏 보면 10000 * 10000 * 10000 * 10000 가지 경우에 대한 brute force를 시도해야 할 것 같다. ~~하지만 문제를 그렇게 내지는 않았겠지.~~

코드를 좀 더 살펴보자.

각 key 값들은 한 번만 사용되고, key 값에 대한 곱셈 및 덧셈 후에 %26 연산을 한다. 나머지 연산은 아래와 같은 성질을 가진다.

  * (a + b) % c = ((a % c) + (b % c)) % c
  * (a * b) % c = ((a % c) * (b % c)) % c

즉, z와 w를 계산할 때, key\[a\]\[b\]에 %26을 먼저 적용하고 계산해도 결과는 동일하다는 뜻이다. 그리고 z와 w는 상호 의존성이 없으므로, brute force할 값의 범위는 26 * 26이 된다.

문제에 flag 값에 pctf가 들어있다고 했으므로 앞에서부터 4글자씩 넣어 보았을 때 pctf가 되는 key 값을 찾아보고, 그걸 이용해서 이후의 문자열을 decrypt 하는 [코드]({{site.github.master}}{{page.rpath}}/ex.py)를 작성하여 돌려보자.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

몇 가지의 가능한 후보 문자열을 얻을 수 있는데, pctf 부분을 떼고 봤을 때 말이 되는 문자열을 submit 했더니 point를 획득할 수 있었다. (submit 할때는 문제에 나와있는대로 pctf{}로 감싸주자.)

Flag : **pctf{ilikeclimbinghillswhataboutyou}**
