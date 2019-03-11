---
layout: post
title: flee button
source: "wargame.kr"
category: Web
rpath: /resource/flee_button
tag: [javascript] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 93

**Author:** Jisoon Park(js00n.park)

**Description:** 

> click the button!
>
> i can't catch it!

## Write-up

문제 페이지에 들어가보면, 버튼을 클릭하라는 텍스트와 마우스 포인터를 따라다니는 버튼이 있다.

물론 문제를 그렇게 냈겠지만, 열심히 마우스 포인터를 움직여 보아도 버튼에 닿지는 않는다.

버튼에 닿았다 치고, 버튼을 눌렀을 때 무슨 일이 생기는지 확인해보자.

chrome의 개발자 도구를 열어보면 관련 코드를 확인할 수 있다.

>![img]({{page.rpath|prepend:site.baseurl}}/src.png)

버튼을 누르면 '?key=57ab'라는 주소로 이동하도록 되어 있다고 한다.

주소표시줄에 해당 주소를 직접 입력하여 이동하면 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **2c21c50674bf9c62d845f4e6fdc41da2242424c2**
