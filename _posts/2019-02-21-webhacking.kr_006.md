---
layout: post
title: webhacking.kr 006
source: "webhacking.kr"
category: Web
rpath: /resource/webhacking.kr_006
tag: [php] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

문제 페이지를 보면 이게 뭐냐 싶다. 일단 소스 코드를 확인하자.

```php
<?php 
if(!$_COOKIE[user]) 
{ 
    $val_id="guest"; 
    $val_pw="123qwe"; 

    for($i=0;$i<20;$i++) 
    { 
        $val_id=base64_encode($val_id); 
        $val_pw=base64_encode($val_pw); 

    } 

    $val_id=str_replace("1","!",$val_id); 
    $val_id=str_replace("2","@",$val_id); 
    $val_id=str_replace("3","$",$val_id); 
    $val_id=str_replace("4","^",$val_id); 
    $val_id=str_replace("5","&",$val_id); 
    $val_id=str_replace("6","*",$val_id); 
    $val_id=str_replace("7","(",$val_id); 
    $val_id=str_replace("8",")",$val_id); 

    $val_pw=str_replace("1","!",$val_pw); 
    $val_pw=str_replace("2","@",$val_pw); 
    $val_pw=str_replace("3","$",$val_pw); 
    $val_pw=str_replace("4","^",$val_pw); 
    $val_pw=str_replace("5","&",$val_pw); 
    $val_pw=str_replace("6","*",$val_pw); 
    $val_pw=str_replace("7","(",$val_pw); 
    $val_pw=str_replace("8",")",$val_pw); 

    Setcookie("user",$val_id); 
    Setcookie("password",$val_pw); 

    echo("<meta http-equiv=refresh content=0>"); 
} 
?> 

<html> 
<head> 
<title>Challenge 6</title> 
<style type="text/css"> 
body { background:black; color:white; font-size:10pt; } 
</style> 
</head> 
<body> 

<? 

$decode_id=$_COOKIE[user]; 
$decode_pw=$_COOKIE[password]; 

$decode_id=str_replace("!","1",$decode_id); 
$decode_id=str_replace("@","2",$decode_id); 
$decode_id=str_replace("$","3",$decode_id); 
$decode_id=str_replace("^","4",$decode_id); 
$decode_id=str_replace("&","5",$decode_id); 
$decode_id=str_replace("*","6",$decode_id); 
$decode_id=str_replace("(","7",$decode_id); 
$decode_id=str_replace(")","8",$decode_id); 

$decode_pw=str_replace("!","1",$decode_pw); 
$decode_pw=str_replace("@","2",$decode_pw); 
$decode_pw=str_replace("$","3",$decode_pw); 
$decode_pw=str_replace("^","4",$decode_pw); 
$decode_pw=str_replace("&","5",$decode_pw); 
$decode_pw=str_replace("*","6",$decode_pw); 
$decode_pw=str_replace("(","7",$decode_pw); 
$decode_pw=str_replace(")","8",$decode_pw); 


for($i=0;$i<20;$i++) 
{ 
    $decode_id=base64_decode($decode_id); 
    $decode_pw=base64_decode($decode_pw); 
} 

echo("<font style=background:silver;color:black>&nbsp;&nbsp;HINT : base64&nbsp;&nbsp;</font><hr><a href=index.phps style=color:yellow;>index.phps</a><br><br>"); 
echo("ID : $decode_id<br>PW : $decode_pw<hr>"); 

if($decode_id=="admin" && $decode_pw=="admin") 
{ 
    @solve(6,100); 
} 


?> 

</body> 
</html> 
```

코드를 살펴보면, id와 pw에 base64 encode를 10번 하고, 1부터 8까지의 숫자들을 특수문자로 대체해서 cookie에 갖고 다니도록 구현되어 있다.

코드 하단에서는 그 연산을 반대로 다시 적용하여 id/pw를 체크한다.

변환 코드를 재활용해서 문제에서 요구하는 cookie에 저장될 적절한 값을 만들어보자.

```php
<?php
//if(!$_COOKIE[user]) 
{ 
    $val_id="admin"; 
    $val_pw="admin"; 

    for($i=0;$i<20;$i++) 
    { 
        $val_id=base64_encode($val_id); 
        $val_pw=base64_encode($val_pw); 

    } 

    $val_id=str_replace("1","!",$val_id); 
    $val_id=str_replace("2","@",$val_id); 
    $val_id=str_replace("3","$",$val_id); 
    $val_id=str_replace("4","^",$val_id); 
    $val_id=str_replace("5","&",$val_id); 
    $val_id=str_replace("6","*",$val_id); 
    $val_id=str_replace("7","(",$val_id); 
    $val_id=str_replace("8",")",$val_id); 

    $val_pw=str_replace("1","!",$val_pw); 
    $val_pw=str_replace("2","@",$val_pw); 
    $val_pw=str_replace("3","$",$val_pw); 
    $val_pw=str_replace("4","^",$val_pw); 
    $val_pw=str_replace("5","&",$val_pw); 
    $val_pw=str_replace("6","*",$val_pw); 
    $val_pw=str_replace("7","(",$val_pw); 
    $val_pw=str_replace("8",")",$val_pw); 

    //Setcookie("user",$val_id); 
    //Setcookie("password",$val_pw); 
	
	echo("ID : $val_id<br>PW : $val_pw<hr>");

    echo("<meta http-equiv=refresh content=0>"); 
}

?>
```

위 코드를 실행시켜보면, 아래와 같은 결과를 얻을 수 있다. (id와 pw는 동일한 값이다.)

![img]({{page.rpath|prepend:site.baseurl}}/run.png)

얻어낸 값을 cookie에 실어 보내면 flag를 얻을 수 있(을 것이)다.

![img]({{page.rpath|prepend:site.baseurl}}/request.png)

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

예전에 풀어놨던거라 flag가 뭔지 모르겠다...(미안)

