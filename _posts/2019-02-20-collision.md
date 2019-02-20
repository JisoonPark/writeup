---
layout: post
title: collision
category: Pwnable
rpath: /resource/collision
tag: [] 
---

**Category:** Pwnable

**Source:** pwnable.kr

**Points:** 30

**Author:** Jisoon Park(js00n.park)

**Description:** 

>Daddy told me about MD5 hash collision today.
>
>I wanna do something like that too!

## Write-up

MD5 hash가 어쩌구 하지만 MD5와는 상관 없는 문제이다. 코드를 보면, 간단한 custom hash 알고리즘이 있고, 의도된 hash값을 만들어내는 문제이다. 

![img]({{page.rpath|prepend:site.baseurl}}/code.png)

main() 함수를 보면 argv[1]로 받아온 20byte의 문자열에 대한 hash를 계산하는데, 이 hash는 입력받은 문자열을 4byte씩 잘라서 정수 형태로 합산한 값이다.

정수 5개를 더해서 어떻게든 0x21DD09EC를 만들어 보자.

strlen() 함수를 이용해서 길이를 검사하므로, 문자열 중간에 0x00은 넣을 수 없다. 대신, 0x01을 16개 넣으면 0x01010101이 4번 들어가서 0x04040404가 될테니, 0x21DD09EC에서 0x04040404를 뺀 0x1DD905E8을 마지막에 넣어주면 된다.

little endian을 고려하여 아래와 같이 넣어주면 간단히 flag 값을 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/run.png)

Flag : **daddy! I just managed to create a hash collision :)**
