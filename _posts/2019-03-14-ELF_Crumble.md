---
layout: post
title: ELF Crumble
category: Reversing
source: "DEFCON CTF 2018 Quals."
rpath: /resource/ELF_Crumble
tag: [elf, binary_patch]
---

**Category**: Reversing

**Source**: DEFCON CTF 2018 Quals.

**Points**: 102

**Author**: Jisoon Park(js00n.park)

**Description:** 

> [pieces.tgz]({{site.github.master}}{{page.rpath}}/pieces.tgz)

## Write-up

압축 파일을 풀어보면 broken이라는 바이너리 파일 하나와 8개의 dat 파일을 얻을 수 있다.

파이너리 파일을 실행해보면 바로 Segmentation Fault가 발생한다.

![img]({{page.rpath|prepend:site.baseurl}}/ida.png)

IDA로 열어보면 main() 함수와 그 위에 있는 f1(), f2(), f3(), recover_flag() 함수가 모두 'pop eax'로만 이루어져 있다. hex view로 살펴보면 파일의 해당 위치가 "X"라는 문자로만 채워져 있는 것을 볼 수 있는데, "X"를 의미하는 0x58을 disassembler가 'pop eax'로 인식한 것임을 알 수 있다.

이 부분을 dat 파일들로 적절히 채워 넣으면 될것 같다. 실제로 dat 파일들의 크기를 다 합치면 807 바이트로, broken 파일에 있는 "X"의 갯수와 동일하다.

이제 dat 파일들을 어떤 순서로 넣으면 좋을지 생각해보자. 친절하게도 정확히 f1() 함수의 시작 위치부터 main() 함수의 마지막 위치까지 비워져 있기 때문에, 첫 위치에 들어갈 파일은 함수의 prologue부터 시작해야 할테고 마지막으로 들어갈 파일은 ret로 끝나야 할 것이다.

![img]({{page.rpath|prepend:site.baseurl}}/first_last.png)

이 조건에 맞는 파일은 다행히 각각 하나씩만 존재한다. 

총 8개의 dat 파일 중에 2개의 위치는 알았으니, 나머지 6개의 위치를 특정해보자.

보통 이런 문제를 풀 때는 call이나 jmp instruction의 jump 주소를 참조하는 경우가 많지만, 이 경우이는 6가지 파일의 조합만 찾으면 되니 그냥 brute force 방식으로 조합을 시도해 보았다. (6! = 720가지 조합)

가능한 모든 조합에 대하여, 각 함수의 시작 주소에 prologue가 있는지 또는 시작 주소 바로 앞에 ret instruction이 있는지 확인해보면 될것 같다.

ret instruction을 확인하는 것을 조건으로 하여 모든 조합을 [확인]({{site.github.master}}{{page.rpath}}/ex.py)하였더니, 조건을 만족하는 한가지 조합이 발견되었고 그 조합을 그대로 실행하여 flag를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **welcOOOme**
