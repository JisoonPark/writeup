---
layout: post
title: type confusion
source: "wargame.kr"
category: Web
rpath: /resource/type_confusion
tag: [php, type_confusion] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 292

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Simple Compare Challenge.
> 
> hint? you can see the title of this challenge.
> 
> :D

## Write-up

하나의 입력창이 주어진다. Javascript 코드를 따라가 보면, util.js 파일의 submit() 함수를 통해 입력값이 json 형태로 서버로 전송되는 것을 확인할 수 있다.

```javascript
function submit(key){
  $.ajax({
    type : "POST",
    async : false,
    url : "./index.php",
    data : {json:JSON.stringify({key: key})},
    dataType : 'json'
  }).done(function(result){
    if (result['code'] == true) {
      document.write("Congratulations! flag is " + result['flag']);
    } else {
      alert("nope...");
    }
    lock = false;
  });
}
```

서버에서는 sha1으로 생성한 key와 내가 전송한 key가 동일한지 비교하게 되는데, sha1() 함수의 반환값은 높은 확률로 문자열일 것으로 기대할 수 있다.

```php
<?php
 if (isset($_GET['view-source'])) {
     show_source(__FILE__);
    exit();
 }
 if (isset($_POST['json'])) {
     usleep(500000);
     require("../lib.php"); // include for auth_code function.
    $json = json_decode($_POST['json']);
    $key = gen_key();
    if ($json->key == $key) {
        $ret = ["code" => true, "flag" => auth_code("type confusion")];
    } else {
        $ret = ["code" => false];
    }
    die(json_encode($ret));
 }

 function gen_key(){
     $key = uniqid("welcome to wargame.kr!_", true);
    $key = sha1($key);
     return $key;
 }
?>
```

문제 이름부터 type confusion이므로, php에서 문자열과 비교했을 때 true가 되는 것들을 찾아보면, true 또는 0임을 알 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/tc.png)

burp suite를 이용해서 POST로 전송되는 json의 key 값을 0으로 수정하였더니 flag를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **5cd960e58d2b53bb5a955167af559dacc578ec3b**

