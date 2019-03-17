---
layout: post
title: You Already Know
category: Web
source: "DEFCON CTF 2018 Quals."
rpath: /resource/You_Already_Know
tag: [개발자도구, XHR]
---

**Category**: Web

**Source**: DEFCON CTF 2018 Quals.

**Points**: 101

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Stop overthinking it, you already know the answer here.
> 
> You already have the flag.
> 
> **Seriously**, if you can read this, then you have the flag.
> 
> Submit it!

## Write-up

(\*. 문제 환경을 재구성하여 풀이하였습니다.)

![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

아무것도 주어진게 없는데 flag를 내놓으라고 한다.

몇가지 가능성을 생각할 수 있을 것 같은데, 우선 소스 코드를 살펴보자. Chrome의 개발자 도구를 이용하면 각종 resource를 쉽게 확인할 수 있다.

flag 형식이 **OOO{}** 라고 하였으니, OOO라는 문자열을 검색해 보았다.

![img]({{page.rpath|prepend:site.baseurl}}/src.png)

소스코드 여기저기를 뒤져봐도 flag 처럼 보이는 것은 없는 것 같다.

다음으로, 웹 문제에서 가장 쉽게 생각해 볼 수 있는 Cookie를 확인해보자.

![img]({{page.rpath|prepend:site.baseurl}}/cookie.png)

Cookie에는 session 정보밖에 없다.

다음으로, Network으로 전송된 정보에 flag가 있는지 확인해보자.

![img]({{page.rpath|prepend:site.baseurl}}/network.png)

Network에도 별 정보가 없다. 이제 뭘 뒤져봐야 하나... 하는데 데이터 중에 Status가 pending인 것이 있다. 잠시 기다리면 200으로 바뀌는데, 그 후에 다시 OOO를 검색해봤더니 문자열 하나가 나왔다.

![img]({{page.rpath|prepend:site.baseurl}}/solve.png)

검색 결과를 더블클릭하여 해당 문자열로 가보면 JSON 형식의 데이터를 볼 수 있다. 브라우저가 XHR(XML Http Request) 요청을 보냈는데, async로 처리하여 회신이 늦게 오도록 한 것 같다.

수신한 데이터는 아래와 같았고, flag가 포함된 것을 확인할 수 있었다. (이 데이터는 수신한 후에 별도로 렌더링 되지 않고 버려진다.)

```
{
    "message": "Stop overthinking it, you already know the answer here.\n\n[comment]: <> (OOO{Sometimes, the answer is just staring you in the face. We have all been there})\n\nYou already have the flag.\n\n**Seriously**, _if you can read this_, then you have the flag.\n\nSubmit it!\n", 
    "success": true
}
```

Flag : **OOO{Sometimes, the answer is just staring you in the face. We have all been there}**
