---
layout: post
title: crack crack crack it
category: Crypto
rpath: /resource/crack_crack_crack_it
tag: [john_the_ripper, md5crypt, mask] 
---

**Category:** Crypto

**Source:** wargame.kr

**Points:** 375

**Author:** Jisoon Park(js00n.park)

**Description:** 

> .htaccess crack!
> 
> can you local bruteforce attack?

## Write-up

패스워드를 잊었다고 하고, .htpasswd 파일이 제공된다. 제공된 파일의 내용은 다음과 같다.

```
blueh4g:$1$3iKA/0.9$AbeqHOgXKAQlQRly3q2R8/
```

인터넷을 검색해보면 .htpasswd 파일은 .htaccess에 대한 암호화를 제공하는 패스워드 파일이라고 한다.

앞의 blueh4g는 id, 뒤의 내용은 암호화된 패스워드인데, 암호화된 패스워드가 $1$로 시작하는건 md5를 이용한 암호화라고 한다. 두번째 $ 이전까지가 salt고 어쩌고 하는데, 알아봐야 별 무소용인 내용이었다.

md5는 대부분 쉽게 복호화할 수 있으니 그렇게 푸는 문제인 줄 알았지만 좀 더 찾아보니 그냥 md5가 아니고, md5 crypt라고 해서 md5를 여러번 돌려서 만드는거라 복호화가 어려워 보였다.

<b>.htpasswd crack</b>으로 검색해 봤더니 주로 JtR(John the Ripper)을 이용하는 것 같았다.

JtR 공부하는셈 치고 옵션을 찾아봤더니 이럴 때 쓸만한 mask 옵션이 있었다.

문제에서 첫 7글자는 주어졌으니 뒤에 많아봐야 한 글자에서 다섯 글자 정도 더 있을거라고 생각하고 옵션을 구성하여 JtR을 돌려보았다.

![img]({{page.rpath|prepend:site.baseurl}}/passwd.png)

생각보다 간단하게 빠른 시간 내에 찾을 수 있었다. 해킹은 툴빨이라더니 역시...

알아낸 비밀번호를 웹페이지에 등록하면 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : <b>b151d5a5957025875c4c811f0bba3b8865aa2026</b>
