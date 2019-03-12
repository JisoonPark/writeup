---
layout: post
title: Help Rabin
category: Crypto
source: "Pragyan CTF 19"
rpath: /resource/Help_Rabin
tag: [Rabin]
---

**Category**: Crypto

**Source**: Pragyan CTF 19

**Points**: 150

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Rabin has received a text from someone special, but it's all in ciphertext and he is unable to make head or tail of it. He requested her for a little hint, and she sent him the encryption algorithm. He's still unable to decode the text. Not wanting to look dumb to her again, he needs your help in figuring out what she's written for him. So help him out.
> 
> [ciphertext.txt]({{site.github.master}}{{page.rpath}}/ciphertext.txt)  
> [publickey.pem]({{site.github.master}}{{page.rpath}}/publickey.pem)  
> [encrypt.py]({{site.github.master}}{{page.rpath}}/encrypt.py)

## Write-up

먼저 encrypt.py 파일을 살펴보자.

```python
[...]

p = getPrime(512)
q = nextPrime(p+1)
while p%4 != 3 or q%4 !=3:
    p = getPrime(512)
    q = nextPrime(p+1)

n = p*q
m = open('secret.txt').read()
m = bytes_to_long(m)

m = m**e
c = (m*m)%n

[...]
```

p와 q는 연속된 prime들이다. 실제로 찾아보면 (크기에 비해서는) 거의 차이가 없는 수이다. n의 square root부터 시작하면 brute-force로 금방 p와 q를 찾을 수 있을 것 같다.

그 다음으로는 d를 계산해서 modular exponentiation을 계산하면 plain text를 얻을 수 있을 텐데, 암호화 과정이 특이하다.  
먼저 e 승을 해주는데, publickey.pem에서 확인해보면 e는 1이다. 그 후에 (m\*m)\%n을 계산하는데 RSA에서라면 e가 2인 셈이 된다. 그런데 조금 생각해보면 알겠지만, RSA에서는 e를 2로 사용하면 안된다. (d를 구할 수가 없다.)

어떻게 푸는 걸까. **RSA public exponent 2**로 [검색](https://crypto.stackexchange.com/questions/65983/rsa-using-2-as-a-public-exponent)을 했더니 [Rabin Cryptosystem](https://en.wikipedia.org/wiki/Rabin_cryptosystem)이라는 얘기가 나왔다. 문제 제목도 Rabin이고 알고리즘을 보아하니 (m\*m)%n으로 암호화 하는 방식도 동일했다.

Rain Cryptosystem의 decryption algorithm에 따라 주어진 ciphertext를 [복호화]({{site.github.master}}{{page.rpath}}/ex.py) 하였더니 4개의 후보값이 나왔고, 그 중의 하나에서 flag를 찾을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **pctf{R4b1n_1s_th3_cut3st}**
