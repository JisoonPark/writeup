---
layout: post
title: webhacking.kr 014
category: Web
rpath: /resource/webhacking.kr_014
tag: [javascript, 개발자도구] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

뭔가 check를 통과할 수 있는 값을 넣어야 하는것 같다.

소스 코드를 찾아보자.

```javascript
<html>
<head>
<title>Challenge 14</title>
<style type="text/css">
body { background:black; color:white; font-size:10pt; }
</style>
</head>
<body>
<br><br>
<form name=pw><input type=text name=input_pwd><input type=button value="check" onclick=ck()></form>
<script>
function ck()
{
var ul=document.URL;
ul=ul.indexOf(".kr");
ul=ul*30;
if(ul==pw.input_pwd.value) { alert("Password is "+ul*pw.input_pwd.value); }
else { alert("Wrong"); }
}

</script>


</body>
</html>

```

check 버튼을 클릭하면 ck() 함수가 호출되고, document.URL()의 ".kr" 문자열의 위치에 30을 곱한 수를 넣어주면 되는 것 같다.

열심히 세어봐도 되지만, 연습할 겸 chrome의 개발자 도구를 사용해 본다.

![img]({{page.rpath|prepend:site.baseurl}}/calc.png)

페이지의 URL은 http://webhacking.kr/challenge/javascript/js1.html 이므로, ".kr"은 17번째 문자임을 알 수 있고, 여기에 30을 곱한 510을 넣어주면 password를 알려준다.

![img]({{page.rpath|prepend:site.baseurl}}/pwd.png)

이 password를 문제목록 상단의 링크를 이용해 auth에 가서 넣어주면 점수를 획득할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

