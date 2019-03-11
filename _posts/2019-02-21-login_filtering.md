---
layout: post
title: login filtering
source: "wargame.kr"
category: Web
rpath: /resource/login_filtering
tag: [php, mysql, case_sensitivity] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 141

**Author:** Jisoon Park(js00n.park)

**Description:** 

> I have accounts. but, it's blocked.
>
> can you login bypass filtering?

## Write-up

ID와 PWD를 입력해서 login을 할 수 있고, 문제의 소스가 제공된다.

소스 코드를 살펴보자.

```php
<?php

if (isset($_GET['view-source'])) {
    show_source(__FILE__);
    exit();
}

/*
create table user(
 idx int auto_increment primary key,
 id char(32),
 ps char(32)
);
*/

 if(isset($_POST['id']) && isset($_POST['ps'])){
  include("../lib.php"); # include for auth_code function.

  mysql_connect("localhost","login_filtering","login_filtering_pz");
  mysql_select_db ("login_filtering");
  mysql_query("set names utf8");

  $key = auth_code("login filtering");

  $id = mysql_real_escape_string(trim($_POST['id']));
  $ps = mysql_real_escape_string(trim($_POST['ps']));

  $row=mysql_fetch_array(mysql_query("select * from user where id='$id' and ps=md5('$ps')"));

  if(isset($row['id'])){
   if($id=='guest' || $id=='blueh4g'){
    echo "your account is blocked";
   }else{
    echo "login ok"."<br />";
    echo "Password : ".$key;
   }
  }else{
   echo "wrong..";
  }
 }
?>
<!DOCTYPE html>
<style>
 * {margin:0; padding:0;}
 body {background-color:#ddd;}
 #mdiv {width:200px; text-align:center; margin:50px auto;}
 input[type=text],input[type=[password] {width:100px;}
 td {text-align:center;}
</style>
<body>
<form method="post" action="./">
<div id="mdiv">
<table>
<tr><td>ID</td><td><input type="text" name="id" /></td></tr>
<tr><td>PW</td><td><input type="password" name="ps" /></td></tr>
<tr><td colspan="2"><input type="submit" value="login" /></td></tr>
</table>
 <div><a href='?view-source'>get source</a></div>
</form>
</div>
</body>
<!--

you have blocked accounts.

guest / guest
blueh4g / blueh4g1234ps

-->
```

mysql_fetch_array를 하기 전에, mysql_real_escape_string() 함수를 이용해서 특수문자를 처리하도록 하고 있다.

mysql_real_escape_string() 함수를 우회할 수 있는 방법을 찾아보면, multibyte encoding을 사용해서 우회할 수 있다고 나오는데, 열심히 삽질해 보았지만 문제를 풀 수 없었다. multibyte 안쓰는걸로...

코드를 다시 자세히 보면, if문에서 $row에 id가 있을 경우, id가 guest 또는 blueh4g인지 확인하고 있는데, $row['id']=='guest'로 쓰는게 아니라, $id와 비교하고 있는 것을 알 수 있다.

알다시피, php에서는 문자열에 대/소문자를 구분한다. 그렇지만, 간과하기 쉬운데, sql query에서는 그렇지 않다. (select ...으로 쓰던 SELECT ...로 쓰던 동일하게 동작한다.)

그러니, php가 다른 문자열이라고 판단하도록 'Guest' 등의 id로 로그인을 시도하면 DB query는 작동하고 if문은 회피할 수 있다.

(솔직히 나는 이걸 생각해내지 못해서 다른 사람의 풀이를 찾아봤다 ㅜㅠ)

ID/PWD 넣는 텍스트박스가 나오면 무조건 SQL INJECTION이라고 생각했었는데, 그런면에서 보면 신선한 문제였다. 왠지 머리가 부드러운(?) 젊고 어린 해커들은 1초만에 풀었을거 같다...

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **63222f28790ea16a173b7a7bc0f1ddcbd73bd08b**
