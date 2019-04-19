---
layout: post
title: Project Eulernt
category: Misc
source: "PlaidCTF 2019"
rpath: /resource/Project_Eulernt
tag: [factorization]
---

**Category**: Misc

**Source**: PlaidCTF 2019

**Points**: 200

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Guys, guys, don’t fight. I’m sure we’ll be able to come up with something roughly equal.
> 
> [source]({{site.github.master}}{{page.rpath}}/eulernt.py)
> 
> eulernt.pwni.ng:5555 

## Write-up

```python
[...]

N = int(gmpy2.fac(333))
#N = 10334465434588059156093965538297516550622260[...]
sN = int(gmpy2.isqrt(N))
#sN = 3214726338988757399964463840205273148284735[...]

k = int(input("Enter number: "))

goodness = Decimal(abs(k - sN)) / sN 

if k and N % k == 0 and goodness < 1e-8:
    print(open('/home/eulernt/flag.txt').read())
elif k and N % k == 0 and goodness < 1e-4:
  print("Good work! You're getting there.")
else:
    print("Nope!")
```

<em>N = 333!</em>이고, <em>sN = sqrt(N)</em>이다. 아래쪽의 if문을 살펴보면, <em>N</em>의 약수 중에 <em>sN</em>과 거의 유사한(10<sup>-8</sup> 정확도) 어떤 수 <em>k</em>를 찾아야 하는 것을 알 수 있다.

N은 333!이니, 1부터 333까지의 숫자를 최대 한번씩만 사용해서 k를 만들어야 조건을 만족할 수 있을 것이다.

문제 제목이 오일러(euler)와 유사하길래 도움이 될만한 수학 공식이 있는지 살펴 보았으나 찾지는 못했다. 그래도 미련을 못버리고 한참을 찾아보다가, 문제 분류가 Misc인 것을 보고 찾는 것을 포기했다.

알고리즘을 생각해보자. <em>a * b == N</em>일 때, a와 b가 비슷한 크기를 가진다면 a와 b는 sN에 가까운 수가 될것이다.

일단 N을 대충이나마 엇비슷하게 반으로 쪼갤 수 있는 알고리즘을 생각해 보았다.

```python
a = 1
b = 1

#1. init
for i in range(2, 333, 2):
  c = abs(a * i - b * (i + 1))
  d = abs(a * (i + 1) - b * i)

  if (c < d):
    #c is better
    a *= i
    b *= i + 1
  else:
    a *= i + 1
    b *= i
```

(2, 3), (4, 5), (6, 7)... 을 번갈아가면서 a와 b에 각각 곱해가는데, a와 b의 차이가 적어지는 방향으로 곱하도록 하였다. 이렇게 해서 a와 b를 구한 후 sN과 비교해 보면 대충 아래와 같은 것을 확인할 수 있다.

```
sN / a = 1.00150466738
sN / b = 0.998497593247
```

아직 갈 길이 멀다. 여기서 어떻게 더 개선을 할 수 있을까 고민하다가, sN에 더 가까워 지기 위해 양쪽에 곱해준 수들을 트레이드 하는 방법을 생각해 보았다. 예를 들면, sN/a = 1.0015이니, a에 곱했던 어떤 수 k1와 b에 곱했던 어떤 수 k2가 <em>k2/k1 = 1.0015</em>를 만족한다면 a에서 k1을 빼고 k2를 곱하면 <em>a == sN</em>이 될 것이다.

먼저, a와 b가 어떤 수들의 곱인지 알 수 있도록 a와 b를 계산할 때 list를 만들었다. 그리고는 2차원 loop을 돌면서 sN/a와 가장 가까운 (k2/k1)의 조합을 찾아서 트레이드를 하도록 하였다.

![img]({{page.rpath|prepend:site.baseurl}}/depth1.png)

... 전혀 개선되지 않았다. 역시나 이렇게 쉽게 풀리진 않을 것 같았다.

선수 풀이 너무 작은 것 같아서, 1:1이 아닌 1:2, 2:1, 2:2 트레이드도 가능하도록 알고리즘을 개선해 보았다. 각 리스트 내에서 1개 또는 2개 원소의 곱으로 만들 수 있는 숫자들을 모두 모아서 새로운 리스트를 만들어 최적의 트레이드 조건을 찾아보았다.

![img]({{page.rpath|prepend:site.baseurl}}/depth2.png)

약간의 시간이 걸리긴 했지만, 괄목할만한 결과를 만들어 내었다. a팀에서 241, 273을 보내고 b팀에서 204, 323을 받아오는 트레이드로, 무려 <em>10<sup>-7</sup></em>의 정확도로 a, b를 찾아낼 수 있었다.

이번엔 최대 3명의 트레이드가 가능하도록 변경하고, 너무 오랜 시간이 걸릴 것이 예상되었기 때문에 종료 조건도 추가해서 다시 실행하였다.([code]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/depth3.png)

다행히 생각보다 오래 걸리지는 않아서(반나절 이상은 걸릴 줄 알았으나) 몇십분 정도 후에 <em>10<sup>-9</sup></em> 이상의 정확도를 갖는 a, b를 찾을 수 있었고, 이를 이용해서 flag를 얻었으나 이미 대회는 종료된 뒤였다(...)

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **PCTF{R3fr3sh1ngly_Sm00th}**

이후에 암호천재님의 조언을 받아 알고리즘을 개선하였다.

  * <em>N = 1 * 2 * 3 * ... * 332 * 333 = 2<sup>238</sup> * 3<sup>165</sup> * 5<sup>81</sup> * ... * 313 * 317 * 331</em>

이므로, <em>sN = sqrt(N)</em>은 아래와 같이 쓸 수 있다.

  * <em>sqrt(N) = 2<sup>119</sup> * 3<sup>82</sup> * 5<sup>40</sup> * ... * sqrt(3 * 5 * ... * 313 * 317 * 331) = x * sqrt(y)</em>

그러므로, 위의 문제 <em>k | N, k &asymp; sN</em>을 만족하는 k 찾기는 <em>k' | y, k' &asymp; sN/x</em>를 만족하는 k'을 찾는 문제로 다시 쓸 수 있다.

생긴건 동일하지만 찾아야 하는 수의 범위가 훨씬 줄어들었다.

기존의 코드에서 크게 변경할 것 없이, 알고리즘의 전단계에서 N을 y로 바꿔주고 sN을 sN/x로 바꾸기만 하면 된다. 다만, 범위가 줄어든 만큼 조합을 찾는 것도 어려워 졌기 때문에 5개의 순서쌍까지 후보에 넣어야 solution을 찾을 수 있었으나, 소요 시간은 훨씬 줄어 1분 내에 알고리즘이 종료되었다.([code]({{site.github.master}}{{page.rpath}}/ex2.py)) [3초짜리 알고리즘]({{site.github.master}}{{page.rpath}}/ex_otherteam.py)은 대체....

![img]({{page.rpath|prepend:site.baseurl}}/run2.png)
