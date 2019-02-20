---
layout: post
title: DLL with notepad
category: Reversing
rpath: /resource/DLL_with_notepad
tag: [] 
---

**Category:** Reversing

**Source:** wargame.kr

**Points:** 428

**Author:** Jisoon Park(js00n.park)

**Description:** 

> DLL Reverse Engineering Challenge.
> 
> Can you reversing DLL File?

## Write-up

주어진 압축파일을 풀어보면, notepad.exe와 blueh4g.dll 파일이 들어있다. 문제 제목이 DLL 리버싱인 만큼, notepad.exe는 쳐다도 안보고 일단 ida로 dll 파일을 열었다.

함수 목록을 쭉 살펴봤을 때, 별달리 두드려볼만한 함수가 보이지 않아 일단 가장 먼저 실행될 DllMain() 함수부터 살펴보았다.

![img]({{page.rpath|prepend:site.baseurl}}/dllmain.png)

fdwReason이 1이면, 즉 라이브러리가 처음 로딩되는 상황이면 start() 함수를 부른다.

![img]({{page.rpath|prepend:site.baseurl}}/start.png)

실행파일 이름이 "notepad.exe"라면 StartAddress() 함수를 실행하는 스레드를 생성한다.

![img]({{page.rpath|prepend:site.baseurl}}/startaddress.png)

드디어 뭔가 출제자가 작성한듯한 코드가 나왔다. 일단 제목이 "blue4g.txt - 메모장"인 프로세스를 찾아서 그게 이 프로세스이면 "edit" 영역에 있는 문자열을 갖고 와서 <b>10003388</b>번지의 값과 비교하도록 하는것 같다. 비교 결과가 동일하다면 String이라는 전역변수에 있는 값을 보여주는 코드로 보인다. (흐리게 표시되는 지역변수 String과 진하게 표시되는 전역변수 String을 구분 못해서 한참 헷갈렸다.) 그렇다면 최종적으로 SetWindowTextA() 함수에서 출력될 값을 찾아보자.

![img]({{page.rpath|prepend:site.baseurl}}/settext.png)

런타임에 0x10001300 번지의 String 값을 확인할 수 있으면 될 것 같다.

IDA 디버깅은 익숙하지 못하니(...) ollydbg를 이용해서 notepad를 열었다.

일단 dll이 로딩된 주소를 확인하기 위해 View - Executable Modules에서 blueh4g.dll 파일의 주소를 확인하여 그쪽으로 이동했다.

![img]({{page.rpath|prepend:site.baseurl}}/address.png)

베이스 주소가 0x6AF10000이라고 하니, IDA에서 확인했던 0x10001300 번지를 보려면 베이스 주소에 0x1300을 더하면 된다. (IDA에서 dll 로딩할 때 베이스 주소를 0x10000000으로 했어서..)

![img]({{page.rpath|prepend:site.baseurl}}/key.png)

이 값을 이제 어디에 써야 하나 한참 고민했는데, 그냥 문제 페이지에 넣으면 flag를 알아낼 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **e71c9d43ba4e78683864c23e16d8fdf4b27e00c1**
