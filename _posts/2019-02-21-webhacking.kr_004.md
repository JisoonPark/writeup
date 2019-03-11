---
layout: post
title: webhacking.kr 004
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_004
tag: [base64, SHA-1] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 150

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

뭔지 모를 코드가 주어지는데, 대소문자 숫자가 섞여있고 ==로 끝나는걸로 봐서는 base64 인코딩된 문자열인것 같다.

일단 디코드 해보면 20바이트의 값인 것을 알 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/decode.png)

20바이트 길이인것으로 미루어 SHA-1의 message digest가 아닐지 의심되어서

레인보우테이블에서 해당 값을 검색해보면 또다른 20바이트 메세지에 대한 hash임을 알 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/reversesha1-1.png)

동일한 방법으로 해당 메세지를 다시 한번 decrypt 하면 test라는 값을 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/reversesha1-2.png)

즉, 주어진 메세지는 "test"라는 문자열을 SHA-1으로 두 번 hash한 값이다.

문제 페이지로 돌아가서, 해당 문자열을 제출하면 flag를 얻을 수 있(을 것이)다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

예전에 풀어놨던거라 flag가 뭔지 모르겠다...(미안)

