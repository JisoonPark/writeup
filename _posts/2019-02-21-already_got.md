---
layout: post
title: already got
category: Web
rpath: /resource/already_got
tag: [http, header] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 88

**Author:** Jisoon Park(js00n.park)

**Description:** 

> can you see HTTP Response header?

## Write-up

HTTP Response header를 볼 수 있냐고 묻는다.

당연히 볼 수 있으므로, flag에 yes를 넣어봤지만 오답이었다.(...)

Response header를 확인하기 위해 burpsuite를 켜고 Start를 누르면 새로운 창이 열린다.

>![img]({{page.rpath|prepend:site.baseurl}}/new_window.png)

burpsuite에서 이 창에 대한 response를 확인해보면 flag가 있는 것을 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **8cb12e8f70f6fdc842fc4492060d9529139484f1**
