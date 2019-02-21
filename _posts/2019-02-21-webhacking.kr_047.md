---
layout: post
title: webhacking.kr 047
category: Web
rpath: /resource/webhacking.047
tag: [email, header] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 150

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

Mail Header Injection 문제이다.

페이지 소스를 열어보면 index.phps가 제공되는 것을 볼 수 있다.

```php
<html>
<head>
<title>Challenge 47</title>
</head>
<body>
Mail Header injection
<pre>
<form method=post action=index.php>
<font size=2>Mail</font> : <input type=text name=email size=50 style=border:0 maxlength=50><input type=submit>
</form>

<?

if($_POST[email])
{

$pass="????";

$header="From: $_POST[email]\r\n";

mail("admin@webhacking.kr","readme","password is $pass",$header);


echo("<script>alert('Done');</script><meta http-equiv=refresh content=1>");
}
?>

</pre>

<!-- index.phps -->

</body>
</html>
```

입력한 이메일 주소를 발송인으로 하여 admin 계정으로 password 정보를 보내도록 되어있다.

제목에서 알려준대로 injection을 하기 위해 우선 email header의 구조를 알아보자.

검색을 통해 email header를 찾아보면 굉장히 여러가지를 넣을 수 있도록 되어있는 것 같은데, 일단 저 메일을 나에게 보내는 것이 목적이니 관련 필드를 찾아보면 To, Cc, Bcc가 있다.

To를 넣어봐야 mail 함수에서 admin@webhacking.kr으로 덮어쓸것 같으니 날아가는 패킷을 잡아 Cc로 원하는 주소를 넣어보자.

![img]({{page.rpath|prepend:site.baseurl}}/request.png)

원래는 내 실제 이메일 주소를 넣어야 하지만, 대충 Cc에 뭔가 다른 주소가 들어오면 password를 알려준다.

알아낸 password를 auth 등록하면 점수를 획득할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)
