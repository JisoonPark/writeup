---
layout: post
title: webhacking.kr 015
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_015
tag: [redirection] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 50

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

문제를 열어보면 "Access Denied"라는 경고창이 뜨고, 확인을 누르면 잠시 텍스트 창이 지나가고 문제 리스트로 돌아간다.

서버가 빠릿빠릿 할때는 순식간에 지나갔을것 같기도 한데, 지금은 몇초 후에(...) 지나간다.

지나가는 텍스트창을 캡쳐해보자.

![img]({{page.rpath|prepend:site.baseurl}}/pwd.png)

password가 off_script라고 한다.

![img]({{page.rpath|prepend:site.baseurl}}/pwd.png)

50점 짜리 문제니까 크게 고민은 하지 말자.

이 password를 문제목록 상단의 링크를 이용해 auth에 가서 넣어주면 점수를 획득할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

