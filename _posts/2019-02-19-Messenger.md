---
layout: post
title: Messenger
category: Crypto
rpath: resource/Messenger
tag: [algebra, extended_euclidean_algorithm] 
---

**Category:** Crypto

**Source:** Samsung CTF 2017 Quals

**Points:** 100

**Author:** Jisoon Park(js00n.park)

**Description:** 

> I made a new Messenger with Identity Based Cryptography.
> 
> The flag is in admin's messages. Can you read it?
> 
> nc 10.113.108.125 30303
> 
> source : Samsung CTF 2017 Quals

## Write-up

우선, 주어진 [IBM.py 파일]({{site.github.master}}/{{page.rpath}}/IBM.py)을 살펴보자.

서비스 시작과 동시에 messages 디렉토리의 admin 파일에 flag를 기록하고,  
pk(public key)와 서버의 sk(secret key)를 생성한다.

![img]({{site.baseurl}}/{{page.rpath}}/setup.gif)

이후 사용자가 register를 요청하면 사용자 ID와 pk, sk를 이용하여 
사용자별 sk를 생성하여 반환해준다.

![img]({{site.baseurl}}/{{page.rpath}}/register.gif)

read 또는 write 요청이 있는 경우에는 (brute-force 공격을 막기 위해 POC 단계를 거친 후) 
사용자 ID와 사용자 sk를 이용하여 로그인 수행 후에 read/write 요청을 수행한다.

![img]({{site.baseurl}}/{{page.rpath}}/login.gif)

read 및 write 기능은 messages/[id] 파일을 통하여 이루어 지므로, register/read/write를 잘 조합하여 
messages/admin 파일의 내용을 읽어 오면 flag를 획득할 수 있겠다.

user_sk 하나만 가지고는 진도를 나가기 힘들어 보인다. register 시도 횟수에는 제한이 없으니 두 개의 
id와 그에 따른 sk를 생성하여, 각각을 sk_a, sk_b라고 하자.

주어진 ID 기반 암호화 시스템은 sk의 비밀성에 기반을 두고 있으니, 서버의 sk만 알 수 있으면 시스템을 
공격할 수 있을 것이다.  
서버의 sk에 지수 연산을 하여 사용자 sk를 생성하고 있으니, 두 개의 사용자 sk를 알고 있으면 
[확장 유클리드 알고리즘(extended euclid algorithm)](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)을 사용하여 서버의 sk를 찾을 수 있을 것으로 여겨진다.

[확장 유클리드 알고리즘](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)을 이용하여 다음을 만족하는 a와 b를 찾는다.  

![img]({{site.baseurl}}/{{page.rpath}}/exeuc.gif)

id1과 id2는 SHA256을 적용 했을 때 서로 소(relative prime)인 id를 사용하면 된다.  
아무거나 몇 번 시도해보면 쉽게 찾을 수 있다.

지수 연산과 곱셈 연산을 통해 다음과 같이 서버의 sk를 찾아낼 수 있다.

![img]({{site.baseurl}}/{{page.rpath}}/findsk.gif)

sk를 찾았으므로, register와 login 및 read 과정을 참고하여 [exploit]({{site.github.master}}/{{page.rpath}}/ex.py)을 작성 후 실행해보면  
admin의 메세지에 있는 flag 값을 찾아낼 수 있다.

![img]({{site.baseurl}}/{{page.rpath}}/flag.png)

Flag : <b>SCTF{Constructing_ID_Based_Cryptosystem_is_so_hard_:(}</b>
