---
layout: post
title: webhacking.kr 024
category: Web
rpath: /resource/webhacking.kr_024
tag: [cookie, str_replace] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

아무것도 안했는데 잘못된 IP라고 나온다... 일단 페이지 소스를 보자.

```html
<html>
<head>
<title>Challenge 24</title>
</head>
<body>
<table border=1><tr><td>client ip</td><td>116.120.157.228</td></tr><tr><td>agent</td><td>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36</td></tr></table><p><hr><center>Wrong IP!</center><hr>


<!--

source : index.phps

-->

</body>
</html>
```

index.phps파일을 열어보면 php 코드를 볼 수 있다고 한다.

```php
<html>
<head>
<title>Challenge 24</title>
</head>
<body>
<?

extract($_SERVER);
extract($_COOKIE);

if(!$REMOTE_ADDR) $REMOTE_ADDR=$_SERVER[REMOTE_ADDR];

$ip=$REMOTE_ADDR;
$agent=$HTTP_USER_AGENT;


if($_COOKIE[REMOTE_ADDR])
{
$ip=str_replace("12","",$ip);
$ip=str_replace("7.","",$ip);
$ip=str_replace("0.","",$ip);
}

echo("<table border=1><tr><td>client ip</td><td>$ip</td></tr><tr><td>agent</td><td>$agent</td></tr></table>");

if($ip=="127.0.0.1")
{
@solve();
}

else
{
echo("<p><hr><center>Wrong IP!</center><hr>");
}
?>



<!--

source : index.phps

-->

</body>
</html>
```

ip라는 변수의 값을 "127.0.0.1"로 맞춰주면 될것 같다.

ip는 REMOTE_ADDR이라는 변수에서 가져오는데, 기본값은 requester의 IP 주소로 설정되는것 같다.

(extract 함수는 dictionary 형식의 데이터를 변수와 변수의 값으로 풀어헤쳐주는(?) 동작을 한다.)

extract($\_SERVER) 실행 이후에 extract($\_COOKIE)가 호출되므로, COOKIE에 REMOTE\_ADDR를 넣어주면 ip 변수의 값을 조절할 수 있을 것 같다.

COOKIE에 REMOTE_ADDR=127.0.0.1을 바로 넣어주면 이후의 str_replace() 구문을 통과하면서 1만 남는다. str_replace() 구문을 통과했을 때 의도했던 문자열이 남도록 "112277..00..00..1"을 넣어주면 "127.0.0.1"이 남으면서 문제를 해결할 수 있게 된다.

![img]({{page.rpath|prepend:site.baseurl}}/modify.png)

원래 문제를 해결했을 때 뭐라고 나왔었는지는 기억나지 않는다.(...)

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

