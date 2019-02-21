---
layout: post
title: webhacking.kr 039
category: Web
rpath: /resource/webhacking.039
tag: [] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

문제를 보니 이것도 injection 문제인것 같다. 소스코드를 보면 index.phps가 있으니 보라고 한다.

감사한(?) 마음으로 열어보자.


```php
<html>
<head>
<title>Chellenge 39</title>
</head>
<body>

<?

$pw="????";

if($_POST[id])
{
$_POST[id]=str_replace("\\","",$_POST[id]);
$_POST[id]=str_replace("'","''",$_POST[id]);
$_POST[id]=substr($_POST[id],0,15);
$q=mysql_fetch_array(mysql_query("select 'good' from zmail_member where id='$_POST[id]"));

if($q[0]=="good") @solve();

}

?>

<form method=post action=index.php>
<input type=text name=id maxlength=15 size=30>
<input type=submit>
</form>
</body>
</html>
```

입력한 id가 DB에 있으면 good이 반환되고 문제가 풀리도록 되어있다.

일단 아무거나 넣어보면 SQL 오류가 발생한다.

![img]({{page.rpath|prepend:site.baseurl}}/error.png)

코드를 자세히 보면, id를 넣는 부분에서 single quot를 열기만 하고 닫지 않는다.

텍스트 박스에 입력할 때 맨 뒤에 single quot를 추가하면 str_replace()에서 single quot를 두개로 바꾸기 때문에 여전히 오류가 나고, \ 를 이용해도 마찬가지로 str_replace()가 지워버리기 때문에 해결할 수가 없다.

코드를 유심히 보면 substr()함수로 15문자를 자르는데, 이걸 이용해서 불필요한 single quot를 잘라낼 수 있을 것 같다.

적당히 있을만한 id인 good이나 admin뒤에 공백을 채우고 15번째 글자를 single quot로 하여 전송하면 str_replace()를 지나면서 잠시 16 글자가 되었다가, substr()에서 다시 15글자가 되어 문제를 해결할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)
