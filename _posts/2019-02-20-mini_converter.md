---
layout: post
title: mini converter
category: Pwnable
rpath: /resource/mini_converter
tag: [ruby, buffer_under_read] 
---

**Category:** Pwnable

**Source:** Codegate 2019 Quals.

**Points:** 21.3

**Author:** Jisoon Park(js00n.park)

**Description:** 

> nc 110.10.147.105 12137 
> 
> [Download]({{site.github.master}}{{page.rpath}}/46e55bdcecb36d86de39571dca6aa013.zip)

## Write-up

ruby에 관련한 문제이다. 일단 서버에 접속해서 뭐하는 프로그램인지 한번 살펴보자.

![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

hexa 문자열, 일반 문자열, 정수 문자열을 받아서 상호간 변환한 값을 돌려주는 프로그램이다.

[코드]({{site.github.master}}{{page.rpath}}/converter_user.rb)는 어떤지 살펴보자.

다행히 ruby script의 문법은 어렵지 않아서 ruby에 대한 사전지식 없이도 쉽게 내용을 알아볼 수 있었다.

```ruby
flag = "FLAG{******************************}"
# Can you read this? really???? lol
```

맨 윗줄에 flag 변수가 선언되어 있는데, 이를 통해서 memory leak을 하면 되는 문제임을 알 수 있다.

[코드]({{site.github.master}}{{page.rpath}}/converter_user.rb)는 정말이지 별게 없었고, 유일하게 혹시나? 싶은 부분이 문자열을 정수 또는 hexa 문자열로 변환해줄 때 사용하는 unpack() 함수였다.

왠지 엄청 긴 문자열을 넣는다던가 할 때 buffer overflow 같은 취약점이 있을 것 같아서 **ruby string unpack vulnerability**로 검색을 해보았더니 **CVE-2018-8778** 취약점에 대한 결과가 많이 검색 되었다.

그 중에 제목부터 "An in-depth look at CVE-2018-8778"로 시작하는 [문서](https://blog.sqreen.io/buffer-under-read-ruby/)가 있어서 내용을 한번 살펴 보았는데, string#unpack의 파라미터 처리과정이 실제로는 C로 구현되어 있어서 strtoul()을 이용해서 길이를 다루는 과정에서 취약점이 발생한다는 내용이 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/ruby_vuln.png)

길이가 unsigned long으로 다뤄지기 때문에 8 byte의 매우 큰 수는 ruby에서는 정상적으로 처리가 되지만 C를 거치면서 underflow가 발생한다는 내용이었다.  
(18446744073709551416 = 2<sup>64</sup> - 200)

조금 더 자세히 말하면 다음과 같은 순서로 underflow가 발생한다.

  [string.unpack()에서 {len}을 처리하는 과정에서]
  1. ruby에서는 길이가 singed long으로 인식되지만 길이 제한이 없어서 over/underflow 일어나지 않음
  2. C에서는 unsigned long으로 인식됨: ff로 시작하는 8 byte data이지만, unsigned라서 정확히 처리됨
  3. 다시 ruby로 올라올 때 C의 unsigned long이 ruby의 signed long으로 casting 되면서 음수로 인식됨

이 underflow는 @ directive와 함께 사용되면서 buffer under-read 취약점이 발생하는데, 이는 @ directive가 data의 parsing을 시작할 위치를 지정하는 지정자로 사용되기 때문이다. 그렇기 때문에 unpack에 @-200 처럼 지정하게 되면 해당 문자열 변수의 200 byte 앞에서 부터 parsing을 시작한다. (물론 이렇게 -200을 직접 집어넣으면 동작하지 않는다.)


그리고 아래와 같은 공격 예시가 있어서 많은 도움이 되었다.

![img]({{page.rpath|prepend:site.baseurl}}/attack.png)

이제, 문제에서 주어진 [코드]({{site.github.master}}{{page.rpath}}/converter_user.rb)에서 unpack을 사용하는 부분을 다시 보자.

```ruby
    elsif flag == 2
      if num == 1
        puts "string to integer"
            STDOUT.flush
            puts input.unpack("C*#{input}.length")
            STDOUT.flush
    
        elsif num == 2
        puts "string to hex"
            STDOUT.flush
            leak = 100
            size = 2**64 - 1 - leak + 1
            puts input.unpack("H*#{input}.length")[0]
            STDOUT.flush
```

내가 입력한 문자열이 {input}으로 들어갈 수 있도록 되어 있다. 원래는 **#{input.length}** 모양이어야 하는데, **.length**가 중괄호 밖으로 빠져나와서 취약점이 생긴 것 같다.

위에서 나온 공격 벡터를 사용하려면 일단 **@** 문자가 필요하고, 그 뒤에 underflow에 필요한 길이를 써준 후, C#{len}을 이용해서 len 만큼의 character를 찍어 memory leak을 하면 될것 같다.  
(여담이지만, 새벽에 머리가 멍한 상태에서 @#{숫자}C#{숫자} 형태로 계속 시도하다가 시간을 많이 날려먹었다. 우리가 쓴 문자열에는 숫자가 그대로 들어가 있으므로 #은 필요하지 않다.)

간단하게 [exploit]({{site.github.master}}{{page.rpath}}/ex.py)을 작성해서 input 변수 이전의 1~2MB에 해당하는 메모리의 dump를 얻었다.  
(더 큰 크기를 요청하면 높은 확률로 요청이 실패한다.)

실행할때마다 프로세스의 메모리 구성이 달라지긴 하지만, printable character만 걸러낸 [데이터]({{site.github.master}}{{page.rpath}}/res.txt)로부터 어렵지 않게 flag를 찾아낼 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **FLAG{Run away with me.It'll be the way you want it}**
