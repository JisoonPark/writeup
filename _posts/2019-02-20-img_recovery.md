---
layout: post
title: img recovery
category: Forensic
rpath: /resource/img_recovery
tag: [png, japng, QR] 
---

**Category:** Forensic

**Source:** wargame.kr

**Points:** 295

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Recovery the PNG image file!
> 
> but.. is this really "PNG" file?
> (NO STEGANOGRAPHY. THIS IS FORENSIC CHALLENGE)

## Write-up

문제 화면에 들어가보면 이미지 패턴이 쭉 보이고 코드를 입력하는 부분이 있다. 별달리 주어지는게 없으니 일단 배경의 이미지를 다운로드 해보면 pattern.png임을 알 수 있다.

문제 설명에 스테가노그래피가 아니라 forensic이라고 나오는걸로 봐서 깨진 이미지인가 싶어 이런저런 이미지 파서로 정보를 살펴보았으나, 별다른 이상을 찾을 수 없었다.

한참을 살펴보다가 다른 png 파일과 비교해 보니, 헤더는 별다를 것이 없는데, footer 부분에 의미 있어보이는 문자열이 있었다. (왼쪽이 문제의 이미지, 오른쪽이 일반 이미지)

![img]({{page.rpath|prepend:site.baseurl}}/compare.png)

**tEXt Software Japng r119**로 검색을 해보니, Japng는 **Java Animated PNG**라는 의미라고 한다. 적당한 japng 분석 도구(https://www.reto-hoehener.ch/japng)를 받아서 이미지를 분석해보니, 이미지가 2장이 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/decode.png)

export해서 비교해보니, 주어진 이미지와는 다르게 보이는 이미지가 한장 더 있었다. 처음에 문제 이미지를 봤을 때부터 QR 코드 이미지가 corrupt 된것 같다고 생각했어서 두 이미지를 겹쳐 보았다.

```python
import Image

background = Image.open("0_pattern.png")
overlay = Image.open("1_pattern.png")

background = background.convert("RGBA")
overlay = overlay.convert("RGBA")

new_img = Image.blend(background, overlay, 0.5)
new_img.save("result.png","PNG")
```
[result.png]

![img]({{page.rpath|prepend:site.baseurl}}/result.png)

합성된 이미지는 역시나 QR 코드 이미지였고, 온라인 QR decoder를 이용해서 encode된 값을 알아낼 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/code.png)

이 값을 문제 페이지에 넣으면 flag를 알아낼 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **4d501245fcd42318cae860e3ce2b1c57384b9627**
