---
layout: post
title: webhacking.kr 054
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_054
tag: [] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

Password를 맞추는 문제인것 같은데, 문제만 봐서는 Password를 알아낼 길이 없다.

일단 소스 코드를 보도록 하자.

```javascript
<html>
<head>
<title>Challenge 54</title>
</head>
<body>
<h1><b>Password is <font id=aview></font></b></h1>
<script>
function run(){
  if(window.ActiveXObject){
   try {
    return new ActiveXObject('Msxml2.XMLHTTP');
   } catch (e) {
    try {
     return new ActiveXObject('Microsoft.XMLHTTP');
    } catch (e) {
     return null;
    }
   }
  }else if(window.XMLHttpRequest){
   return new XMLHttpRequest();
 
  }else{
   return null;
  }
 }

x=run();

function answer(i)
{
x.open('GET','?m='+i,false);
x.send(null);
aview.innerHTML=x.responseText;
i++;
if(x.responseText) setTimeout("answer("+i+")",100);
if(x.responseText=="") aview.innerHTML="?";
}

setTimeout("answer(0)",10000);

</script>
</body>
</html>
```

가장 먼저 run 함수가 보이는데, 코드를 보면 XMLHttpRequest() 객체임을 알 수 있다. 서버에 뭔가를 request해서 받아오는 소켓 같은 건가보다.

그리고 answer 함수가 있는데, 마지막에 보면 10초 후에 answer(0)를 호출하도록 되어 있다.

answer 내부를 살펴보면, i를 1씩 증가시키면서 setTimeout() 함수를 이용해 0.1초마다 answer(i)를 호출하고 있는 것을 알 수 있다.

i를 증가시켜 가다가 서버에서 더이상의 응답을 보내주지 않으면 ?를 출력하고 끝내는것까지이다.

뭔가 공격자가 끼어들 건덕지가 없는 것 같다. 다시 문제 페이지로 돌아가서, 페이지를 새로 고침하고 기다리면 10초 정도 후에 글자가 하나 나타나고, 잠깐씩의 텀을 두면서 계속 바뀌어 나가는 것을 볼 수 있다.

마지막에 ?가 출력될때까지 보이는 문자열을 순서대로 기록하고, 이를 auth 페이지에 입력하면 이 문제에 대한 점수를 획득할 수 있다.

(다른 사람들의 writeup을 보았을 때, Password는 자주 바뀌는것 같다.)
