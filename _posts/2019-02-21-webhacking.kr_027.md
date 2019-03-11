---
layout: post
title: webhacking.kr 027
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_027
tag: [sql_injection, like] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 150

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

SQL INJECTION 문제이다.

페이지 소스를 보면 index.phps가 제공된다고 쓰여있으므로, 일단 한번 열어보자.


```php
<html>
<head>
<title>Challenge 27</title>
</head>
<body>
<h1>SQL INJECTION</h1>
<form method=get action=index.php>
<input type=text name=no><input type=submit>
</form>
<?
if($_GET[no])
{

if(eregi("#|union|from|challenge|select|\(|\t|/|limit|=|0x",$_GET[no])) exit("no hack");

$q=@mysql_fetch_array(mysql_query("select id from challenge27_table where id='guest' and no=($_GET[no])")) or die("query error");

if($q[id]=="guest") echo("guest");
if($q[id]=="admin") @solve();

}

?>
<!-- index.phps -->
</body>
</html>
```

no=([입력값]) 부분에 전송한 입력이 들어가는데, 바로 윗라인에 이런저런 필터가 있다.

특이한 점은 입력값을 괄호가 싸고 있다는 점인데, 필터를 보면 닫는 괄호는 필터링 하지 않는 것을 알 수 있다. 대충 괄호를 닫고 뒤의 괄호는 주석처리 하라는 뜻인것 같다.

불러와야 하는 id는 admin인데, where 절에서 id='guest' and no=() 라고 되어있으므로, or 구문을 만들어서 admin을 선택하면 될것 같은데, 등호(=) 기호도 필터링 되고 있어서, 비슷하게 사용되는 like 문을 이용하였다.

일단 문제 페이지에서 이런저런 숫자를 넣어보면 guest의 no는 1인것을 알 수 있고, admin은 대충 0 아니면 2일 것을 예상해 볼 수 있다.

앞부분이 true가 되면 안되기 때문에 1이 아닌 값으로 시작해서 공격벡터를 만들면 된다. 아래와 같은 값을 넣어 보면 문제를 풀 수 있다.

<pre>0) or no like 2 -- </pre>

(-- 기호 뒤에 공백을 반드시 넣어줘야 주석문이 제대로 동작한다.)

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

like를 알면 금방 풀고 모르면 알때까지 못푸는 문제인듯...
