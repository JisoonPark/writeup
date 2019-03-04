---
layout: post
title: Who do I trust?
category: Misc
source: "TAMUctf 2019"
rpath: /resource/Who_do_I_trust
tag: [certificate]
---

**Category**: Misc/SSL Certificate

**Source**: TAMUctf 2019

**Points**: 194

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Who issued the certificate to tamuctf.com?  
> (Not in standard gigem{flag} format)
> 
> Difficulty: easy

## Write-up

tamuctf.com의 인증서를 누가 발급했는지 묻고 있다.

주소표시줄 옆의 자물쇠 마크를 클릭하여 인증서 정보를 얻어보자.

![img]({{page.rpath|prepend:site.baseurl}}/ssl.png)

인증서 정보를 보면 발급자 정보를 바로 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/cert.png)

Flag : **Let's Encrypt Authority X3**
