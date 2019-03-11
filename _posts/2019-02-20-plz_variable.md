---
layout: post
title: plz variable
source: "wargame.kr"
category: Misc
rpath: /resource/plz_variable
tag: [polynomial, z3] 
---

**Category:** Misc/Polynomial Solving

**Source:** wargame.kr

**Points:** 682

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Can you find the solution quickly in polynomials?
> 
> nc wargame.kr 10004

## Write-up

nc로 문제 서버에 접속해보면 아래와 같은 메세지를 받을 수 있다.
```
matta@JSPARK-SURFACE:~/matta/GDrive/current/wargame.kr/plz_variable$ nc wargame.kr 10004
Please match the correct answer 30 times.
Submit format -> a,b,c,d,,,(Ascending order)
Timeout = 60sec
a,b,c,d,,, is natural number
a,b,c,d,,, is 100 <=  <= 1000

1th...
b - c - a + d = -230
c * b + d * a = 388688
d + b - c + a = 378
d + c + a + b = 2122
Answer ->
```

60초 내에 30개의 1차 다항식 문제를 풀면 되는 문제이다. 몇번 시도해 보면 미지수의 갯수만큼 다항식이 주어지는 것을 알 수 있다.

이 다항식들과 미지수의 범위(100 <= x <= 1000)를 이용해서 각 미지수를 구해보자.

python polynomial로 검색을 해보면 sage, sympy, numpy, scipy 등 다항식 풀이를 지원하는 다양한 라이브러리들을 볼 수 있는데, sage와 sympy 등으로 문제를 풀려고 해보았지만 잘 되지 않았다.  
(너무 오래 걸리거나 ~~왠지 모르지만~~ 값이 이상하게 나오거나..)

이런저런 검색 끝에 z3 solver를 찾았는데, 이거 좀 좋은거 같다 ㅋㅋㅋ

문제에서 원하는 바가 굉장히 명확하므로, [exploit]({{site.github.master}}{{page.rpath}}/ex.py)에 대한 설명으로 writeup을 대신한다.

```python
for idx in range(30):
  print "====================="
  print r.recvuntil("th...\n")
  print "=====================\n"

  eqs = r.recvuntil("-> ")
  print eqs

  eqs = [l.replace("=", "==") for l in eqs.split("\n")[:-1]]
```

다항식은 **_n_ th...**라는 메세지 이후로 나오므로, 이전의 메세지는 버리고 마지막 **Answer -> **까지의 데이터의 각 라인에서 방정식을 얻는다. (마지막 Answer가 있는 라인은 버린다.)

```python
  variables = list(set(re.findall(r"[a-z]","".join(eqs))))
  variables.sort()
```

방정식에서 등장하는 소문자 알페벳을 모아 (set을 이용하여) 중복을 제거하고 오름차순으로 정렬한다.

```python
  solver = z3.Solver()

  for var in variables:
    exec("%c = z3.Int('%c')"%(var,var))
    solver.add(eval("%s >= 100"%var))
    solver.add(eval("%s <= 1000"%var))

  for eq in eqs:
    solver.add(eval(eq))

```

z3 solver를 선언하고, 미지수 선언과 동시에 각 미지수에 대한 범위 부등식을 solver에 추가한다. 그리고 나서 문제에서 주어진 각 다항식 또한 solver에 추가한다.

변수 선언을 자동으로 하기 위해 exec()를 사용하였고, solver는 다항식을 문자열로 받지 않기 때문에 eval()을 사용하였다.

이 부분에서 삽질을 꽤 했는데, z3의 미지수 변수와 for문의 반복 변수를 동일하게 쓰는 바람에 문제가 생겼었다.  
(그래서 변수 이름이 평소와 달리 다 두글자 이상이다... 설마.. 그래서 문제 이름이?!)  
exec()로 변수 선언을 할때는 이런 부분을 꼭 주의하도록 하자.

```python
  #solve!
  solver.check()
  ans = solver.model()
```

solver에 필요한 식이 모두 추가되면 check() 메소드를 이용해 해를 구한다. model()을 이용하면 해(solution)를 저장하고 있는 model reference에 대한 instance를 얻을 수 있다.

```python
  resp = []
  for var in variables:
    resp.append(str(ans.evaluate(eval(var)).as_long()))

  r.sendline(",".join(resp))
```

model reference는 range, int, boolean 등 다양한 형태의 해를 가질 수 있기 때문에, 적절한 방법을 통해 추출해야 한다.

여기서는 각 미지수의 값을 정수(long)로 가져와서 문자열 리스트의 형태로 저장한 후 문제 서버로 전송하였다.

for문에 따라 30번의 문제를 푼 결과 flag를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **wmkr{Wow_Fuck_the_z3?!}**
