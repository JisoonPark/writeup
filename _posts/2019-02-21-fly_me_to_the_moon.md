---
layout: post
title: fly me to the moon
category: Web
rpath: /resource/fly_me_to_the_moon
tag: [javascript, obfuscation, beautifier, burp_suite] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 200

**Author:** Jisoon Park(js00n.park)

**Description:** 

> javascript game.
>
> can you clear with bypass prevent cheating system?

## Write-up

간단한(?) 웹게임 해킹 문제이다.

좌우로 움직이는 벽을 피하는 게임인데, 한번 죽어보면 31337점을 획득해야 한다는 메세지가 뜬다.

게임 코드는 난독화 되어있는데, 연습 겸 분석해보자.

![img]({{page.rpath|prepend:site.baseurl}}/src1.png)

코드는 eval() 함수를 이용하도록 되어있다. eval() 함수에 주어지는 입력을 확인하기 위해서, eval을 document.write로 수정한 후 chrome의 개발자 도구에서 실행시켜 보면 일련의 소스 코드를 얻을 수 있다.

아직 좀 복잡하게 생겼으니, 적당한 beautifier를 찾아서 한번 더 정리해주면 좀 예쁜 코드를 볼 수 있다.

```javascript
function secureGame() {
    var _0x8618x2 = this;
    var _0x8618x3 = true;

    /************/
    /* 중간 생략 */
    /************/

        if (BTunnelGame['checkLife']()) {
            setTimeout('updateTunnel()', 10)
        } else {
            $('img#ship')['fadeOut']('slow');
            $('img.left_wall')['css']('display', 'none');
            $('img.right_wall')['css']('display', 'none');
            $['ajax']({
                type: 'POST',
                url: 'high-scores.php',
                data: 'token=' + token + '&score=' + BTunnelGame['getScore'](),
                success: function(_0x8618x19) {
                    showHighScores(_0x8618x19)
                }
            })
        }
    };

    /************/
    /* 중간 생략 */
    /************/

    var token = '';

    function updateToken() {
        $['get']('token.php', function(_0x8618x20) {
            token = _0x8618x20
        })
    };
```

코드를 보면 checklife 해서 token과 score를 보내는 곳이 있고, token을 업데이트 하는 곳이 있다. token은 token.php를 이용해서 otp 형식으로 업데이트 되는것 같다. (burp suite에서도 확인할 수 있다.)

burp suite의 repeater를 이용해서 token을 다시 받아오고, 이 token과 함께 31337이라는 score를 보내 보면 "TOKEN ERROR - by. cheating prevention system"라는 에러 메세지를 만날 수 있다.

실제 게임이 동작하는 와중에 보내야 될 것 같은데, 더 분석하기는 귀찮으니 burp suite의 Match and Replace 기능을 이용해보자.

![img]({{page.rpath|prepend:site.baseurl}}/edit.png)

request body에 score=?를 만족하는 문자열이 보이면 점수를 바꿔서 보내도록 해두었다.

다시 게임을 시작한 후, 적당히 빨리 죽어주면 flag를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **13d93b28b53d08b1bd9f43c497b390c7b9593943**
