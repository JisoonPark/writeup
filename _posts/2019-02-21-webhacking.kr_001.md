---
layout: post
title: webhacking.kr 001
category: Web
rpath: /resource/webhacking.kr_001
tag: [php] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 200

**Author:** Jisoon Park(js00n.park)

**Description:** 

>level : 1

## Write-up

```php
<?
if(!$_COOKIE[user_lv])
{
SetCookie("user_lv","1");
echo("<meta http-equiv=refresh content=0>");
}
?>
<html>
<head>
<title>Challenge 1</title>
</head>
<body bgcolor=black>
<center>
<br><br><br><br><br>
<font color=white>
---------------------<br>
<?

$password="????";

if(eregi("[^0-9,.]",$_COOKIE[user_lv])) $_COOKIE[user_lv]=1;

if($_COOKIE[user_lv]>=6) $_COOKIE[user_lv]=1;

if($_COOKIE[user_lv]>5) @solve();

echo("<br>level : $_COOKIE[user_lv]");

?>
<br>
<pre>
<a onclick=location.href='index.phps'>----- index.phps -----</a>
</body>
</html>
```

[php 코드]({{site.github.master}}{{page.rpath}}/index.phps)를 보면 cookie의 user_lv 값을 5보다 크게 하면 되는것 같다.

다만, 바로 윗라인에서 user_lv의 값이 6 이상일 때는 user_lv를 초기화하므로,

아래와 같이 5보다 크고 6보다 작은 수를 적당히 넣어주면 된다.

![img]({{page.rpath|prepend:site.baseurl}}/edit1.png)

burp suite에서 request를 잡아서 cookie의 user_lv를 5.5로 수정하였다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

예전에 풀어놨던거라 flag가 뭔지 모르겠다...(미안)

