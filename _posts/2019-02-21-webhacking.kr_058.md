---
layout: post
title: webhacking.kr 058
category: Web
rpath: /resource/webhacking.058
tag: [flash, decompile] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 150

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

flash로 작성된 문제이다.(문제를 열었을 때 flash를 허용할거냐고 묻는다.)

페이지 소스를 분석해 보면 hackme.swf 파일을 여는 것을 알 수 있다.

>![img]({{page.rpath|prepend:site.baseurl}}/src.png)

일단 다운로드 받아서 swf 디컴파일을 시도해보자. (ffdec라는 좋은 오픈소스가 있다.)

>![img]({{page.rpath|prepend:site.baseurl}}/flash_src.png)

디컴파일을 해서 script 항목에 있는 코드를 확인해보면 쉽게 암호를 알아낼 수 있다.

암호를 입력하면 점수를 획득할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)
