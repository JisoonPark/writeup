---
layout: post
title: webhacking.kr 020
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_020
tag: [javascript, burp_suite] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 200

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

javascript challenge라고 한다. 일단 코드를 봐야겠다.

```javascript
<html>
<head>
<title>Challenge 20</title>
<style type="text/css">
body { background:black; color:white; font-size:10pt; }
input { background:silver; color:black; font-size:9pt; }
</style>
</head>
<body>
<center><font size=2>time limit : 2</font></center>
<form name=lv5frm method=post>
<table border=0>
<tr><td>nickname</td><td><input type=text name=id size=10 maxlength=10></td></tr>
<tr><td>comment</td><td><input type=text name=cmt size=50 maxlength=50></td></tr>
<tr><td>code</td><td><input type=text name=hack><input type=button name=attackme value="fhyjznwusm"
 style=border:0;background=lightgreen onmouseover=this.style.font=size=30 onmouseout=this.style.font=size=15></td></tr>
<tr><td><input type=button value="Submit" onclick=ck()></td><td><input type=reset></td></tr>
</table>
<script>
function ck()
{

if(lv5frm.id.value=="") { lv5frm.id.focus(); return; }
if(lv5frm.cmt.value=="") { lv5frm.cmt.focus(); return; }
if(lv5frm.hack.value=="") { lv5frm.hack.focus(); return; }
if(lv5frm.hack.value!=lv5frm.attackme.value) { lv5frm.hack.focus(); return; }

lv5frm.submit();

}
</script>

<br>

do not programming!<br>

this is javascript challenge

</body>
</html>
```

nickname과 comment에 적당한 값을 넣고 code에 바로 옆에 있는 텍스트를 똑같이 넣으면 submit이 정상적으로 수행된다.

submit 후에 특별한 동작은 없고(잠깐 Wrong이라는 메세지가 보였다가 사라진다.), 해당 페이지가 새로고침 되는데, code에 넣어야 할 값은 이전과 다른 값으로 변경된다. (페이지를 그냥 새로고침해도 마찬가지이다.)

자동으로 계속 submit을 하도록 하면 해결되는 문제인가 싶기도 하지만, 바로 아래에 programming이 아니라고 하는걸 보니 그렇게 푸는건 아닌가보다. 다른 방향을 고민해 보자.

아무리 생각해도 다른 방향은 안떠오르는데, 위에 보면 "time limit : 2"라는 문구가 있다. 2초 안에 submit을 해야하나 보다.

매번 다르게 들어오는 문자열을 어떻게 바로 회신할 수 있을지.. python으로 proxy를 짜야하나 아니면 chrome의 개발자 도구에 이벤트를 추가하거나 하는 방법이 있나 고민해보았지만 마땅치가 않아서 burp suite를 이용했다.

![img]({{page.rpath|prepend:site.baseurl}}/script.png)

위 그림과 같이, script 태그가 감지되면 form을 채우고 바로 ck 함수를 부르는 코드를 삽입하도록 하였다.

이후 다시 문제 페이지를 불러오면 페이지가 계속 리로딩이 되는데(당연히), response를 보면 문제를 해결했다는 회신을 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

근데 이런식이면 programming이 아니라는 말은 구라 아닌가...
