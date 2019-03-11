---
layout: post
title: webhacking.kr 016
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_016
tag: [javascript, key_code] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

문제 페이지를 열어보면 처음에 큰 별 하나와 작은 별 하나가 보인다. 키보드로 아무 글자를 입력하면 별이 늘어나고, 늘어난 별에 커서를 갖다대면 별이 사라진다.

잘 모르겠으니, 일단 소스 코드를 열어보자.

```html
<html>
<head>
<title>Challenge 16</title>
<body bgcolor=black onload=kk(1,1) onkeypress=mv(event.keyCode)>
<font color=silver id=c></font>
<font color=yellow size=100 style=position:relative id=star>*</font>
<script> 
document.body.innerHTML+="<font color=yellow id=aa style=position:relative;left:0;top:0>*</font>";

function mv(cd)
{
kk(star.style.posLeft-50,star.style.posTop-50);
if(cd==100) star.style.posLeft=star.style.posLeft+50;
if(cd==97) star.style.posLeft=star.style.posLeft-50;
if(cd==119) star.style.posTop=star.style.posTop-50;
if(cd==115) star.style.posTop=star.style.posTop+50;
if(cd==124) location.href=String.fromCharCode(cd);
}


function kk(x,y)
{
rndc=Math.floor(Math.random()*9000000);
document.body.innerHTML+="<font color=#"+rndc+" id=aa style=position:relative;left:"+x+";top:"+y+" onmouseover=this.innerHTML=''>*</font>";
}

</script>
</body>
</html>
```

mv와 kk 함수 두가지가 있는데, 천천히 살펴봐도 뭔가 취약점이라던가 하는건 없어 보인다.

mv 함수에서 key code에 따라 특정한 동작을 하는 if문들이 있는데, key code가 124이면 다른 페이지로 이동하도록 되어있다.

javascript의 event.keyCode를 검색해서 살펴보아도 124에 해당하는 문자가 어떤 것인지 알아낼 수 없었다.

뭐, 중요한건 String.fromCharCode(cd)일테니, chrome의 개발자 모드에서 124에 해당하는 문자를 확인해 본다.

![img]({{page.rpath|prepend:site.baseurl}}/124.png)

확인해보면, | 문자인걸 알 수 있다. 혹시나 싶어 문제 페이지에서 |를 입력하면 바로 password를 보여주는 페이지로 이동한다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

이 password를 문제목록 상단의 링크를 이용해 auth에 가서 넣어주면 점수를 획득할 수 있다.
