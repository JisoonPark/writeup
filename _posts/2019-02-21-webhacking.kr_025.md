---
layout: post
title: webhacking.kr 025
category: Web
rpath: /resource/webhacking.kr_025
tag: [file_include, php, null_terminaor] 
---

**Category:** Web

**Source:** webhacking.kr

**Points:** 150

**Author:** Jisoon Park(js00n.park)

**Description:** 

>![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

## Write-up

파일 목록과 텍스트가 주어진다. 소스 코드를 봐도 별다른게 없는데, 주소표시줄을 보면 file=hello라고 되어있다.

hello.txt 파일의 크기는 12 byte이고, 출력된 메세지도 (엔터까지 세면) 12 byte이므로, hello.txt 파일의 내용이 보여지는걸로 생각된다.

file=hello.txt가 아닌 것이 이상하지만, 일단 file=password.php를 넣어서 시도해보았을 때 형편좋게 password가 출력되어 주지는 않는다.

아래의 메세지 창이 hello.txt를 보여주는게 맞다면 전송한 file 문자열에 ".txt"를 붙여서 보여주는걸로 일단 가정해 보자.

password.php를 입력하면 "password.php.txt" 파일을 보여주려고 시도하게 되고, 실패하기 때문에 아마 기본인 hello.txt를 보여주는 것 같다.

php의 string concatenation을 무력화 하기 위해 password.php 뒤에 문자열 종료 문자(0x00)을 강제로 넣어보자.

file=password.php%00을 입력했을 때 정상적으로 password.php 파일의 내용이 표시되는 것을 볼 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

획득한 password를 auth 창에 등록하면 포인트를 획득할 수 있다.
