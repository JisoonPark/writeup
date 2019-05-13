---
layout: post
title: REDACTED-PUZZLE
category: Misc
source: "DEFCON CTF 2019 Qulas."
rpath: /resource/REDACTED-PUZZLE
tag: [git]
---

**Category**: Misc

**Source**: DEFCON CTF 2019 Qulas.

**Points**: Not fixed yet

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Everything you need is in this file.
> 
> Files: [redacted-puzzle.gif]({{site.github.master}}{{page.rpath}}/redacted-puzzle.gif)

## Write-up

필요한 모든게 파일에 있다고 하는데 막상 열어보면 아무것도 보이지 않는다.

010editor로 살펴보면 파일 구조에는 별다른 특이사항이 없다.

![img]({{page.rpath|prepend:site.baseurl}}/header.png)

인터넷에서 평범한 gif 파일들을 다운받아 헤더 부분을 비교해 보았더니 헤더의 Color Table 부분이 대부분 0x00으로 적혀있는 부분이 이상해보여 이 부분을 대충 다른 값으로 덮어 보았다.

![img]({{page.rpath|prepend:site.baseurl}}/header2.png)

다시 파일을 열어보았더니 움직이는 gif 파일임을 확인할 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/redacted-puzzle_edited.gif)

각 프레임은 flag는 32 종류의 글자로 이루어져있다는 말과 함께 8각형의 임의의 꼭지점들을 이은 도형들로 이루어져 있었다.

이 [gif 파일]({{site.github.master}}{{page.rpath}}/redacted-puzzle_edited.gif)을 적당한 [사이트](https://ezgif.com/split)에서 frame 별로 나누어 보았더니 총 [35 프레임]({{site.github.master}}{{page.rpath}}/redacted-puzzle_fames.zip)인 것을 확인할 수 있었다.

이미지가 8각형을 그린다는 점에서 각 꼭지점이 특정 bit을 나타내는 것일거라고 가정하고 각 frame에서 몇 번째 꼭지점이 선택되어 있는지 모아 보았다. (왼쪽 위 꼭지점을 0번으로 하여 시계방향으로 순서를 부여하였다.)

이미지를 파싱하여 자동으로 수집할까 생각해 보았으나 자세히보면 이미지가 조금씩 회전하고 있어서 그냥 손으로 적었다.

한 frame에서 8bit 씩 35 frame에서 총 280 bit의 데이터를 확인했는데, 이 데이터를 어떻게 flag로 바꿀 수 있을지 고민하다가, the13님의 조언에 따라 (flag가 32가지 글자로 이루어져 있으니까) 5bit씩 묶어서 flag 구성 문자열의 index로 사용해보았더니 flag를 얻을 수 있었다.([code]({{site.github.master}}{{page.rpath}}/ex.py))

(msb의 index가 0인 것으로 계산해야 제대로 된 flag를 얻을 수 있었다.)

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **OOO{FORCES-GOVERN+TUBE+FRUIT_GROUP=FALLREMEMBER_WEATHER}**
