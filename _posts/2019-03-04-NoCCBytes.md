---
layout: post
title: NoCCBytes
category: Reversing
source: "TAMUctf 2019"
rpath: /resource/NoCCBytes
tag: [decompile, gdb]
---

**Category**: Reversing

**Source**: TAMUctf 2019

**Points**: 491

**Author**: Jisoon Park(js00n.park)

**Description:** 

> nc rev.tamuctf.com 8188
> 
> Difficulty: medium
> 
> [noccbytes.pyc]({{site.github.master}}{{page.rpath}}/noccbytes)

## Write-up

실행해봐도 별거 없다. 일단 main() 함수를 살펴보자.

![img]({{page.rpath|prepend:site.baseurl}}/main.png)

뭔지 모를 check() 함수를 지나고 나서 입력받은 값을 passCheck() 함수에서 체크한다.  
이 체크만 잘 넘기면 flag를 보여준단다.

passCheck() 함수도 살펴보자.

![img]({{page.rpath|prepend:site.baseurl}}/passcheck.png)

여기서도 역시 뭔지 모를 check() 함수를 지나고나서 globPass에 있는 문자열과 입력한 문자열을 비교하여 결과를 리턴하도록 되어있다.

앞에서 뭐 어떻게 되건 별 관심없고, 최종적으로 비교하게 되는 globalPass 변수에 어떤 값이 들어가는지 gdb를 통해 확인해보자. (**hi**는 내가 입력한 값이다.)

![img]({{page.rpath|prepend:site.baseurl}}/globPass.png)

서버에 접속 후 globalPass 변수에 들어있던 **WattoSays**를 입력해주면 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **gigem{Y0urBreakpo1nt5Won7Work0nMeOnlyMon3y}**
