---
layout: post
title: Flag collision
category: Misc
source: "ASIS CTF 2019 Quals"
rpath: /resource/Flag_collision
tag: [crc32, collision]
---

**Category**: Misc/Coding

**Source**: ASIS CTF 2019 Quals

**Points**: 67

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Warm-up your fingers to capture next flags!
> 
> nc 37.139.9.232 19199
## Write-up

![img]({{page.rpath|prepend:site.baseurl}}/prob.png)

주어진 사이트에 접속해보면 먼저 PoW(Proof Of Work)을 요구한다. PoW는 sha1, sha2, md5의 다양한 hash 알고리즘에 대해서 나오는데, PoW를 풀고 나면 본격적인 문제가 나온다.

주어진 길이에 따라 두 개의 ASIS CTF flag 형식의 문자열을 생성하면 되는데, 두 문자열의 CRC32 값이 같아야 한다고 한다.

CRC32 collision generator를 찾아보다가 [이 사이트](https://www.nayuki.io/page/forcing-a-files-crc-to-any-value)에서 [forcecrc32.py]({{site.github.master}}{{page.rpath}}/forcecrc32.py)를 찾았는데, 이 라이브러리는 특정 파일에서 주어진 위치의 4 바이트를 수정하여 원하는 CRC32 값을 갖도록 해주는 기능을 갖고 있다.

해당 파일을 받아서 아래와 같이 변경하였다.[(code)]({{site.github.master}}{{page.rpath}}/crc.py)

  * 파일명 입력 --> 데이터 입력
  * 길이를 입력받아 ASIS CTF flag 형태의 임의의 문자열 s1, s2 생성 후, crc32(s2)가 crc32(s1)과 동일해지도록 s2를 수정

조건에 맞는 s1, s2를 구해서 서버로 전송하면 동일한 형태의 길이만 다른 다음 문제가 나온다.

loop을 이용하여 계속 문제를 풀어나가다 보면 flag를 얻을 수 있다.[(code)]({{site.github.master}}{{page.rpath}}/ex.py)

![flag]({{site.github.master}}{{page.rpath}}/flag.png)

Flag : **ASIS{3asy_c0din9_fOr_W4rM_UP}**
