---
layout: post
title: Open-gyckel-krypto
category: Crypto
source: "Midnightsun CTF 2019"
rpath: /resource/Open-gyckel-krypto
tag: [RSA]
---

**Category**: Crypto

**Source**: Midnightsun CTF 2019

**Points**: 226

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Primes are fun, don't google translate me bro
> 
> Download: [gyckel.tar.gz]({{site.github.master}}{{page.rpath}}/gyckel.tar.gz)
> 
> Author: grocid is available for questions in #midnightsun @ freenode  
> Status: Online

## Write-up

(uphack 팀의 [writeup](https://upbhack.de/posts/2019/04/writeup-open-gyckel-krypto-from-midnightsun-ctf-2019-quals/)을 참조하였습니다.)

주어진 텍스트 파일을 열어보면 간단한 python 코드와 RSA 공개키, 그리고 암호문을 찾을 수 있다.

```python
while True:
    p = next_prime(random.randint(0, 10**500))
    if len(str(p)) != 500:
        continue
    q = Integer(int(str(p)[250:] + str(p)[:250]))
    if q.is_prime():
        break

>> p * q
61460246439415037572177153632567252974745825[...]
>> pow(m, 65537, p * q)
35720309045280131806911840318258750185600188[...]
```

500자리 10진수 소수인 p를 생성하고, 상위 250자리와 하위 250자리를 바꾼 값이 q라고 한다. 상위와 하위를 각각 250 자리의 십진수 a, b라고 하고 식으로 쓰면 아래와 같다.

  * <em>p = a * 10<sup>250</sup> + b</em>
  * <em>q = b * 10<sup>250</sup> + a</em>

문제에서 n = pq 값이 주어지는데, 이 값을 a, b로 써보면 아래와 같다.
  * <em>n = pq = (a * 10<sup>250</sup> + b)(b * 10<sup>250</sup> + a) = ab * 10<sup>500</sup> + (a<sup>2</sup> + b<sup>2</sup>) * 10<sup>250</sup> + ab</em>

![img]({{page.rpath|prepend:site.baseurl}}/leng.png)

a와 b가 각각 250 자리의 수이니, <em>a<sup>2</sup></em>는 최대 500 자리이고, <em>a<sup>2</sup> + b<sup>2</sup></em>는 500자리 수이거나 1로 시작하는 501자리 수가 될 것이다.

<em>x = ab, y =  a<sup>2</sup> + b<sup>2</sup></em>라고 하면, 1000자리 십진수인 pq는 위의 식에 따라 아래와 같이 구성될 것이다.

```
xxxxxxxxxxxxxxxxxxxx
         cyyyyyyyyyyyyyyyyyyyy
                    xxxxxxxxxxxxxxxxxxxx

 where carry c is 0 or 1
```

위의 pq를 x와 y에 대해 다시 쓰면 <em>pq = x * 10<sup>500</sup> + y * 10<sup>250</sup> + x</em>가 된다. 500 자리의 x에서 상위 250자리와 하위 250자리를 (carry를 고려하면) 50% 확률로 알아낼 수 있다. x를 알아내고 나면 pq, x, y에 대한 식을 정리해서 y의 값도 알아낼 수 있다.

RSA 비밀키를 얻기 위해서는 <em>phi(N) = (p - 1)(q - 1)</em>의 값을 알아내야 한다. 

  * <em>phi(N) = (p - 1)(q - 1) = pq + 1 - (p + q)</em>
  * <em>p + q = (a + b) * 10<sup>250</sup> + (a + b)</em>

위와 같이 정리해보면 최종적으로 알아내야 하는 값은 a + b인 것을 알 수 있다.

<em>x = ab, y = a<sup>2</sup> + b<sup>2</sup></em>의 값을 알고 있으므로, sqrt(y + 2x)를 계산하면 a + b를 알아낼 수 있다.(<em>a + b</em>는 정수이므로, <em>y + 2x</em>가 제곱수인지 확인해보면 x, y를 제대로 찾았는지 확인할 수 있다.)

  * <em>sqrt(y + 2x) = sqrt(a<sup>2</sup> + b<sup>2</sup> + 2ab) = sqrt((a + b)<sup>2</sup>)</em>

<em>a + b</em>를 알아내고 나면 phi(N), d, m을 순서대로 계산하여 flag를 얻을 수 있다.([code]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **midnight{w3ll_wh47_d0_y0u_kn0w_7h15_15_4c7u4lly_7h3_w0rld5_l0n6357_fl46_4nd_y0u_f0und_17_50_y0u_5h0uld_b3_pr0ud_0f_y0ur53lf_50_uhmm_60_pr1n7_7h15_0n_4_75h1r7_0r_50m37h1n6_4nd_4m4z3_7h3_p30pl3_4r0und_y0u}**
