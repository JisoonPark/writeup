---
layout: post
title: keypad CrackMe
category: Reversing
rpath: /resource/keypad_CrackMe
tag: [time] 
---

**Category:** Reversing

**Source:** wargame.kr

**Points:** 376

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Simple Reverse Engineering Challenge.

## Write-up

실행파일이 주어지고, 실행해보면 뭔가 숫자를 입력하고 auth를 해야하는것 같다.

아무거나 넣어보면 wrong password라고 얘기해준다.

decompile을 시도한 후 wrong password 문자열을 찾아본다.

![img]({{page.rpath|prepend:site.baseurl}}/string.png)

이 문자열을 사용하는 함수를 디컴파일 해보면 대충 아래와 같은 코드를 얻을 수 있다.

```c
//(생략...)

  Time = _time64(0);
  v2 = *((_DWORD *)v1 + 29);
  v3 = (const wchar_t **)((char *)v1 + 116);
  v4 = *(_DWORD *)(v2 - 12);
  if ( ((1 - *(_DWORD *)(v2 - 16 + 12)) | (*(_DWORD *)(v2 - 16 + 8) - v4)) < 0 )
    ((void (__stdcall *)(int))sub_C22420)(v4);
  v5 = _wtoi(*v3);
  if ( _localtime64_s(&Tm, &Time) )
    v6 = 0;
  else
    v6 = Tm.tm_mon + 1;
  if ( 0xFFFCECC9 * v6 + v5 == 0xBADBABE )
  {
    AfxMessageBox(L"congratulations! Authentication key is .....", 0, 0);

//(생략...)
```

_wtoi() 함수를 이용하는걸 보면 keypad로 입력한 값이 v5에 저장되는것 같다.

if문을 true로 만드려면 v6를 알아야 하는데, v6는 _locatime64_s() 함수의 리턴값과 동작 내용으로 알아낼 수 있을 것 같다.

MS api 페이지를 참조해보면, _locatime64_s() 함수는 시간 데이터를 구조체에 채워주고, 성공하면 0을 리턴한다고 한다. 뭐 이런 시스템 함수가 실패할거 같지는 않고, else 절을 보면 Tm.tm_mon을 이용하는데, 지금이 12월이니 11이 될것 같다.(보통 month 데이터는 0~11로 표현되니까)

v6 = 11 + 1 = 12가 될거고, 이걸로 if 문을 만족시키는 v5를 역산해 보면 0xbd2a152를 얻을 수 있다. 이를 decimal로 변환하여 198353234를 입력하면 keypad 하단의 입력창에서 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **1567d027bf68fc0ab316728628e8ed3a45189ef8**

그냥 대충 위치만 잡고 디버거에서 if-true branch를 타도록 해도 될거 같았지만 그냥 리버싱 연습하는 의미에서 간단하게나마 코드 분석으로 진행했다.
