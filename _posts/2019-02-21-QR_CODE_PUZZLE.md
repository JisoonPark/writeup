---
layout: post
title: QR CODE PUZZLE
category: Web
rpath: /resource/QR_CODE_PUZZLE
tag: [QR] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 116

**Author:** Jisoon Park(js00n.park)

**Description:** 

> javascript puzzle challenge
>
> just enjoy!

## Write-up

문제 페이지에 들어가보면, QR 코드 이미지를 6x6으로 분할한 조각 퍼즐이 나온다.

아무 생각 없이 퍼즐을 풀다가, 이렇게 푸는게 아니라는 생각이 들었다.

먼저, 페이지 소스 코드를 확인해 본다.

```javascript
<center>
<script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js'></script>
<script type="text/javascript" src="jquery.jqpuzzle.js"></script>
<script type='text/javascript' src='jquery.color-RGBa-patch.js'></script>
<script type='text/javascript' src='jquery.blockUI.js'></script>
<script type="text/javascript">
/*<![CDATA[*/
 $(function(){ $('#join_img').attr('src',unescape('.%2f%69%6d%67%2f%71%72%2e%70%6e%67'));
  $('#join_img').jqPuzzle({rows:6,cols:6,shuffle:true,numbers:false,control:false,style:{overlap:false}});
  hide_pz();});
 function hide_pz(){
  var pz=$('#join_img div'); if(pz[pz.length-2]){$(pz[1]).remove();$(pz[pz.length-2]).remove();}else{setTimeout("hide_pz()",5);}
 }
/*]]>*/
</script>
<style>
#join_img {padding:15px 15px 0 15px; border:2px solid #999; background-color:#444;}
</style>
<br />
<h1>QR Code Puzzle</h1>
<br />
<img id="join_img" /><br />
```

마지막에 보면 join_img를 보여주는데, javascript에 보면 뭔가 의심스러운 url 인코딩 된 문자열이 보인다.

![img]({{page.rpath|prepend:site.baseurl}}/url_decode.png)

url decode해보면, "./img/qr.png"라는 경로가 보이는데, 이걸 따라 "http://wargame.kr:8080/qr_code_puzzle/img/qr.png" 페이지로 가보면 원본 qr 코드 이미지를 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/qr.png)

원본 qr 코드 이미지를 찾았으니, 대충 아무 온라인 qr decoder를 이용하여 decoding을 수행해본다.

![img]({{page.rpath|prepend:site.baseurl}}/qr_decode.png)

decoding 된 qr 코드는 하나의 URL을 던져주는데, 이 URL로 접속해보면 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **59c4ea27083762adab514956704844c720dc4508**
