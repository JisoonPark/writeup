---
layout: post
title: Cookie Monster
category: Web
source: "Pragyan CTF 19"
rpath: /resource/Cookie_Monster
tag: [cookie]
---

**Category**: Web

**Source**: Pragyan CTF 19

**Points**: 100

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Do prepare to see cookies lurking everywhere.
> 
> http://159.89.166.12:13500/

## Write-up

미리 Burp suite proxy를 설정하고 문제 페이지에 들어가 보았다.

![img]({{page.rpath|prepend:site.baseurl}}/response.png)

response에 flag를 지정하는 데이터가 실려온다.

이게 왜 100점이지 하면서 submit 해보았으나 flag가 아니었다. 뭔가 한번 처리를 해야 하나 보다.

막상 들여다보니 ascii data도 아니어서, 다른 데이터 형인가 싶어 검색해 보았더니 문자열 "pc"에 대한 md5 hash 결과였다.

"pc"를 다시 제출해 보았으나 이것도 올바른 flag가 아니었다. 생각해보니 flag 형식이 **pctf()** 이니, flag의 첫 두글자인 것 같다. 나머지 글자들은 어떻게 얻을 수 있을까 고민하다가 새로고침을 했더니, cookie의 flag가 업데이트 되었는데, 역시나 "tf"에 대한 md5 hash였다.

첫번째로 얻은 md5 hash가 다시 나올때까지 계속 request하는 [코드]({{site.github.master}}{{page.rpath}}/ex.py)를 만들어서 돌려봤더니, 아래와 같은 md5 hash들을 얻을 수 있었다.

```
bc54f4d60f1cec0f9a6cb70e13f2127a
114d6a415b3d04db792ca7c0da0c7a55
b2984e12969ad3a3a2a4d334b8fb385a
6f570c477ab64d17825ef2d2dfcb6fe4
988287f7a1eb966ffc4e19bdbdeec7c3
0d4896d431044c92de2840ed53b6fbbd
f355d719add62ceea8c150e5fbfae819
12eccbdd9b32918131341f38907cbbb5
639307d281416ad0642faeaae1f098c4
96bc320e4d72edda450c7a9abc8a214f
c716fb29298ad96a3b31757ec9755763
51de5514f3c808babd19f42217fcba49
05cb7dc333ca611d0a8969704e39a9f0
bc781c76baf5589eef4fb7b9247b89a0
ff108b961a844f859bd7c203b7366f8e
2349277280263dff980b0c8a4a10674b
0b1cdc9fe1f929e469c5a54ffe0b2ed5
364641d04574146d9f88001e66b4410f
c758807125330006a4375357104f9a82
fcfdc12fb4030a8c8a2e19cf7b075926
440c5c247c708c6e46783e47e3986889
97a7bf81a216e803adfed8bd013f4b85
c1d12de20210d8c1b35c367536e1c255
a8655da06c5080d3f1eb6af7b514e309
```

이 hash들에 대한 message를 얻어보았더니 flag를 구성하는 데이터들을 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/md5.png)

각 글자들을 순서대로 조합하면 flag를 얻을 수 있다.  
(No Match라고 나온 hash들은 다른 사이트에서 값을 찾았다.)

Flag : **pctf{c0oki3s_@re_yUm_bUt_tHEy_@ls0_r3vEaL_@_l0t}**
