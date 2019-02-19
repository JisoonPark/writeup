---
layout: post
title: Simon and Speck Block Ciphers
category: Crypto
rpath: /resource/Simon_and_Speck_Block_Ciphers
tag: [simon, brute_force] 
---

**Category:** Crypto

**Source:** SECCON CTF 2017 Quals.

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Simon and Speck Block Ciphers
>
> Simon_96_64, ECB, key="SECCON{xxxx}", plain=0x6d564d37426e6e71, cipher=0xbb5d12ba422834b5
>
> source : SECCON CTF 2017 Quals.

## Write-up

Simon and Speck 암호를 이용한 문제이다.

Simon 암호화, 96bit Key와 64bit Block을 갖는 모드에서 Plain Text와 Cipher Text를 기반으로 Key를 찾는 문제이다.

Key의 4byte만 가려져 있으므로 Brute-Forcing을 이용해서 키를 확인한다.  
(애초에 4byte만 가려져 있다는 점에서 암호 알고리즘 자체의 취약점을 찾는 문제가 아니라는 것을 유추할 수 있다.)

문제에서 Simon and Speck 암호의 스펙이 제공되는데, 인터넷에서 간단히 구현체를 찾아서 다운로드 하였다. 다운로드 한 코드에서 테스트 부분을 수정하여 Brute-forcing을 수행하면 된다.

![img]({{page.rpath|prepend:site.baseurl}}/code.png)

실행시켜보면 약간의 시간이 흐른 후 flag를 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **SECCON{6Pz0}**
