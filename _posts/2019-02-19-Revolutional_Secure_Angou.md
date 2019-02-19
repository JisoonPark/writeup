---
layout: post
title: Revolutional Secure Angou
category: Crypto
rpath: /resource/Revolutional_Secure_Angou
tag: [RSA, brute_force] 
---

**Category:** Crypto

**Source:** TokyoWesterns CTF 2018

**Points:** 154

**Author:** Jisoon Park(js00n.park)

**Description:** 

> (None)

## Write-up

별도의 문제 설명은 주어지지 않았다. 주어진 ruby 코드를 살펴보자.

```ruby
require 'openssl'

e = 65537
while true
  p = OpenSSL::BN.generate_prime(1024, false)
  q = OpenSSL::BN.new(e).mod_inverse(p)
  next unless q.prime?
  key = OpenSSL::PKey::RSA.new
  key.set_key(p.to_i * q.to_i, e, nil)
  File.write('publickey.pem', key.to_pem)
  File.binwrite('flag.encrypted', key.public_encrypt(File.binread('flag')))
  break
end
```

RSA-2048 keypair를 생성하는데, 오리지널 알고리즘과는 다르게 p와 q 사이에 의존성이 있다.  
이후의 코드에 별다른 특이점이 보이지 않는 것으로 보아, 이 의존성을 이용하는 문제인것 같다.

p는 1024bit 난수이고, q는 e의 p에 대한 역수이므로, 다음과 같이 쓸 수 있다.

q = e<sup>-1</sup> mod p  
=> eq = 1 mod p  
=> eq = kp + 1

p와 q가 비슷한 크기(bit length)의 수라고 하면, k와 e도 비슷한 크기를 가질 것이다. e가 65537로 17 bit의 수이니, k도 brute force를 이용해서 찾을 수 있을 정도의 크기라고 생각해 볼 수 있다.

식을 좀 더 정리해보자.

eq = kp + 1  
=> eqq = kpq + q  
=> eqq - q - kpq = 0  
=> eq<sup>2</sup> - q - kN = 0  

q에 대한 2차 방정식을 얻었다. 2차 방정식 ax<sup>2</sup> + bx + c = 0 의 해는 근의 공식으로 구할 수 있다. 기억이 가물가물하니 잠시 추억을 되살려보자.

![img]({{page.rpath|prepend:site.baseurl}}/quadratic_formula.png)

얻어진 식을 근의 공식에 대입해보면, a = e, b = -1, c = -kN 이다.

q는 정수이므로, 근의 공식에서 제곱근 계산 결과가 정수이어야 하고, 분자 부분은 분모의 배수이어야 한다. 이 성질을 이용해서 k를 찾기 위해 아래와 같은 exploit을 작성하였다.

((a, b) = iroot(c, d)는 c의 d 제곱근을 구하는 함수이며, 계산 결과a와 제곱근이 정수인지 나타내는 boolean 값인 b를 리턴한다.)

```python
from Crypto.PublicKey import RSA
from gmpy2 import iroot
from Crypto.Util.number import *

keypair_pem = open("publickey.pem", "r").read()
keypair = RSA.importKey(keypair_pem)

ct = open("flag.encrypted", "rb").read()

t = 4 * keypair.e * keypair.n
for k in range(1, 1000000):
  (y, b) = iroot(1 + t * k, 2)
  if b and (1 + y) % (keypair.e * 2) == 0:
    print k
    q = (1 + y) // (keypair.e * 2)
    break

p = keypair.n // q
piN = (p - 1) * (q - 1)

d = inverse(keypair.e, piN)

'''
pt = pow(bytes_to_long(ct), d, keypair.n)
print long_to_bytes(pt)
'''
#same as above
priv = RSA.construct((keypair.n, keypair.e, long(d)))
print priv.decrypt(ct)

#RSAES-PKCS1_v1_5 padding example
from Crypto.Cipher import PKCS1_v1_5
cipher = PKCS1_v1_5.new(priv)
print cipher.decrypt(ct, 0)

```

간단한 brute forcing 만으로 k는 쉽게 찾을 수 있었다.  
(p에 대한 2차 방정식으로 정리해도 동일하게 풀 수 있다.)

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

plain RSA를 이용해서 decryption 했을 때 앞에 지저분한(?) 것들이 보이고 뒤에 flag 같은게 보인다. hex 값을 찍어보면 0x02로 시작하는 걸로 보아 ruby에서 RSAES-PKCCS#1_v1.5 padding을 붙인 것 같다.  
그냥 flag만 발췌해도 되지만 나중에 참고용으로 RSAES-PKCCS#1_v1.5 decryption code도 [exploit]({{site.github.master}}{{page.rpath}}/ex.py)에 포함했다.

Flag : <b>TWCTF{9c10a83c122a9adfe6586f498655016d3267f195}</b>
