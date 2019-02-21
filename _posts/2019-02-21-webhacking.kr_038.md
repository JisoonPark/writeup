---
layout: post
title: webhacking.kr 038
category: Web
rpath: /resource/webhacking.038
tag: [data_injection] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

LOG를 injection하는 문제이다.

뭔소린지 잘 모르겠다...

일단, 아무 값이나 넣고 login을 테스트 해보면 별다른 동작이 수행되지 않는다.

Admin 버튼을 눌러보면 그동안 입력했던 값들이 로그 형태로 표시된다.

![img]({{page.rpath|prepend:site.baseurl}}/log.png)

admin으로 로그인을 시도해 보면 admin이 아니라고 오류를 낸다.

![img]({{page.rpath|prepend:site.baseurl}}/error.png)

늘 그렇듯이 admin을 따면 뭔가 될것 같다.

로그를 다시 보고 php가 생성해낸 값을 정확히 알기 위해 소스를 확인해본다.

```html

<html>
<head>
<title>log viewer</title>
</head>
<body>
<!--

hint : admin

-->
log<br>115.145.170.90:admin1
<br>211.36.147.139:f
<br>211.36.147.139:f
<br>219.254.222.210:abc
<br>219.254.222.210:def
<br><br></body>
</html>

```

무슨 의미가 있는지는 잘 모르겠지만, 제목이 LOG INJECTION인걸 보니 admin으로 정상 로그인한 것처럼 로그를 넣어보고 싶어진다.


마지막 로그를 따서 abc&lt;br&gt;219.254.222.210:admin 을 넣어보자.

로그인을 해봐도 별달리 수행되는게 없는 것같다. 다시 Admin버튼으로 로그를 확인해보면 어느샌가 풀려있는 문제를 볼 수 있다....

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)
