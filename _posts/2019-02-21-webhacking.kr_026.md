---
layout: post
title: webhacking.kr 026
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_026
tag: [url_encode] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

문제 페이지를 열어보면 일단 소스코드를 보라고 한다.

```php
<html> 
<head> 
<title>Challenge 26</title> 
<style type="text/css"> 
body { background:black; color:white; font-size:10pt; }     
a { color:lightgreen; } 
</style> 
</head> 
<body> 

<? 

if(eregi("admin",$_GET[id])) { echo("<p>no!"); exit(); } 

$_GET[id]=urldecode($_GET[id]); 

if($_GET[id]=="admin") 
{ 
@solve(26,100); 
} 

?> 


<br><br> 
<a href=index.phps>index.phps</a> 
</body> 
</html>
```

urldecode를 했을 때 "admin"이 되는 문자열을 넣어달라고 한다.

burp suite의 Decoder 도구를 이용해서 "admin" 문자열을 urlencode하자.

![img]({{page.rpath|prepend:site.baseurl}}/urlencode.png)

urlencode한 문자열을 GET을 통해 보내도록 되어 있는데, urlencode를 한번 한 문자열을 그대로 보내면 php에는 자동으로 decode 되어 전달된다.

자동으로 decode 되어도 문제 코드에서 다시 한번 urldecode를 수행했을 때 정상적으로 "admin" 문자열을 얻을 수 있도록 urlencode를 두번 수행한다.

얻어낸 문자열 %25%36%31%25%36%34%25%36%64%25%36%39%25%36%65을 아래와 같이 GET 메소드를 이용해서 전송하면 점수를 획득할 수 있다.

<pre>http://webhacking.kr/challenge/web/web-11/?id=%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65</pre>

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

