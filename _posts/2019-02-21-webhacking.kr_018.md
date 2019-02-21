---
layout: post
title: webhacking.kr 018
category: Web
rpath: /resource/webhacking.kr_018
tag: [sql_injeciton, filtering] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

이름부터 친절하게 SQL INJECTION 문제이다.

출제자가 매우 친절한지 소스코드 링크까지 바로 보여준다. 봐주는게 예의.

```php
<html> 
<head> 
<title>Challenge 18</title> 
<style type="text/css"> 
body { background:black; color:white; font-size:10pt; } 
input { background:silver; } 
a { color:lightgreen; } 
</style> 
</head> 
<body> 
<br><br> 
<center><h1>SQL INJECTION</h1> 
<form method=get action=index.php> 
<table border=0 align=center cellpadding=10 cellspacing=0> 
<tr><td><input type=text name=no></td><td><input type=submit></td></tr> 
</table> 
</form> 
<a style=background:gray;color:black;width:100;font-size:9pt;><b>RESULT</b><br> 
<? 
if($_GET[no]) 
{ 

if(eregi(" |/|\(|\)|\t|\||&|union|select|from|0x",$_GET[no])) exit("no hack"); 

$q=@mysql_fetch_array(mysql_query("select id from challenge18_table where id='guest' and no=$_GET[no]")); 

if($q[0]=="guest") echo ("hi guest"); 
if($q[0]=="admin") 
{ 
@solve(); 
echo ("hi admin!"); 
} 

} 

?> 
</a> 
<br><br><a href=index.phps>index.phps</a> 
</cener> 
</body> 
</html> 
```

텍스트박스로 입력하는 값이 no로 넘어간다. 1을 넣어보면 'hi guest'라는 메세지가 나오는 것으로 보아, guest의 no는 1인걸 알 수 있다.

admin의 no는 아마도 0이거나 2일 것이다. admin 계정을 얻기 위해서는 sql query의 where 절에 "... or id=0" 정도의 문자열을 넣어줘야 할텐데, fetch 바로 윗 라인에 필터링 구문이 있다.

sql 쿼리에서 공백을 대체하는 문자로는 \n(0x0a), \t(0x09), \a(0x0d), /\*\*/, (), + 등이 있다고 하는데, 필터링 구문에서 걸러내는 문자열을 제외해서 대충 아무거나 넣어보면 될것 같다.

만만한 \n을 사용해보자. \n 문자열을 그대로 텍스트박스에 넣으면 %5Cn로 인코딩되어 전송되므로, 특수문자 전송을 위해 주소표시줄에 %0a으로 URL 인코딩한 문자열을 보낸다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

원래 뭐라고 나왔었는지는 기억이 안난다.(...)
