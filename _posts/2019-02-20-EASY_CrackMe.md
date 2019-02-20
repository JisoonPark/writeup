---
layout: post
title: EASY_CrackMe
category: Reversing
rpath: /resource/EASY_CrackMe
tag: [IDA] 
---

**Category:** Reversing

**Source:** wargame.kr

**Points:** 312

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Simple Reverse Engineering Challenge.

## Write-up

실행 파일이 주어지고, 실행해보면 뭔가 비밀번호를 넣어야 한다고 한다. 아무거나 넣어보면 "nono.."라는 메세지 박스가 나온다.

![img]({{page.rpath|prepend:site.baseurl}}/nono.png)

ida로 리버싱을 시작해보자. 일단 "nono.."라는 문자열이 사용되는 곳을 찾아 따라간 후에 decompile을 시도했더니 아래와 같은 코드를 얻을 수 있었다. (문자열이 보이지 않는다면 strings window에서 우클릭 - Setup으로 들어가 Allowed string types 하단의 Unicode에 체크해주면 된다.)

![img]({{page.rpath|prepend:site.baseurl}}/strings.png)

```c
int __thiscall sub_B416C0(CWnd *this)
{
  CWnd *v1; // edi@1
  char v2; // bl@1
  const wchar_t *v3; // eax@1
  signed int v4; // esi@1
  wchar_t *v5; // eax@4
  const wchar_t *v6; // eax@9
  wchar_t *v7; // eax@10
  int v8; // esi@15
  DWORD v9; // eax@15
  int v10; // eax@17
  const CHAR *v11; // eax@21
  wchar_t **v12; // eax@23
  int v13; // eax@23
  LPCSTR v14; // eax@28
  wchar_t *v15; // eax@30
  int v17; // [sp+0h] [bp-4Ch]@1
  char v18; // [sp+14h] [bp-38h]@15
  int v19; // [sp+28h] [bp-24h]@23
  CWnd *v20; // [sp+2Ch] [bp-20h]@1
  DWORD pcchUnescaped; // [sp+30h] [bp-1Ch]@15
  wchar_t *v22; // [sp+34h] [bp-18h]@28
  LPCSTR lpMultiByteStr; // [sp+38h] [bp-14h]@19
  int *v24; // [sp+3Ch] [bp-10h]@1
  int v25; // [sp+48h] [bp-4h]@15

  v24 = &v17;
  v1 = this;
  v20 = this;
  v2 = 1;
  CWnd::UpdateData(this, 1);
  v3 = (const wchar_t *)*((_DWORD *)v1 + 30);
  v4 = *((_DWORD *)v3 - 3);
  if ( v4 <= 12 )
    v2 = 0;
  if ( *((_DWORD *)v3 - 3) < 0 || (v5 = wcsstr(v3, L"_my_b")) == 0 || ((signed int)v5 - *((_DWORD *)v1 + 30)) >> 1 == -1 )
    v2 = 0;
  if ( _wtoi(*((const wchar_t **)v1 + 30)) != 1114 )
    v2 = 0;
  v6 = (const wchar_t *)*((_DWORD *)v1 + 30);
  if ( *((_DWORD *)v6 - 3) < 0 || (v7 = wcsstr(v6, L"birth")) == 0 || ((signed int)v7 - *((_DWORD *)v1 + 30)) >> 1 == -1 )
    v2 = 0;
  if ( v4 < 14 && v2 )
  {
    CInternetSession::CInternetSession((struct CInternetSession *)&v18, 0, 1, 0, 0, 0, 0);
    v25 = 0;
    LOBYTE(v25) = 1;
    sub_B41EF0(L"http://wargame.kr:8080/prob/18/ps.php?p=");
    LOBYTE(v25) = 2;
    sub_B41A40(*((wchar_t **)v1 + 30), *(_DWORD *)(*((_DWORD *)v1 + 30) - 12));
    v8 = sub_B53072(pcchUnescaped, 1u, 0x80000002, 0, 0);
    LOBYTE(v25) = 1;
    v9 = pcchUnescaped - 16;
    if ( _InterlockedDecrement((volatile signed __int32 *)(pcchUnescaped - 16 + 12)) <= 0 )
      (*(void (__stdcall **)(DWORD))(**(_DWORD **)v9 + 4))(v9);
    v25 = 0;
    sub_B41EF0(&word_C961F8);
    LOBYTE(v25) = 4;
    v10 = sub_B485E9();
    if ( !v10 )
      sub_B422A0(-2147467259);
    lpMultiByteStr = (LPCSTR)((*(int (__thiscall **)(int))(*(_DWORD *)v10 + 12))(v10) + 16);
    LOBYTE(v25) = 5;
    if ( v8 )
    {
      while ( (*(int (__thiscall **)(int, LPCSTR *))(*(_DWORD *)v8 + 88))(v8, &lpMultiByteStr) )
      {
        v11 = lpMultiByteStr;
        if ( *((_DWORD *)lpMultiByteStr - 1) > 1 )
        {
          sub_B42020(*((_DWORD *)lpMultiByteStr - 3));
          v11 = lpMultiByteStr;
        }
        v12 = (wchar_t **)sub_B41600((int)&v19, v11);
        LOBYTE(v25) = 6;
        sub_B41A40(*v12, *((_DWORD *)*v12 - 3));
        LOBYTE(v25) = 5;
        v13 = v19 - 16;
        if ( _InterlockedDecrement((volatile signed __int32 *)(v19 - 16 + 12)) <= 0 )
          (*(void (__stdcall **)(int))(**(_DWORD **)v13 + 4))(v13);
      }
    }
    else
    {
      sub_B42190(L"sorry, server is down.. but you clear this crackme!!", 52);
    }
    AfxMessageBox(L"G00d!", 0, 0);
    AfxMessageBox(v22, 0, 0);
    LOBYTE(v25) = 4;
    v14 = lpMultiByteStr - 16;
    if ( _InterlockedDecrement((volatile signed __int32 *)lpMultiByteStr - 1) <= 0 )
      (*(void (__stdcall **)(LPCSTR))(**(_DWORD **)v14 + 4))(v14);
    LOBYTE(v25) = 0;
    v15 = v22 - 8;
    if ( _InterlockedDecrement((volatile signed __int32 *)v22 - 1) <= 0 )
      (*(void (__stdcall **)(wchar_t *))(**(_DWORD **)v15 + 4))(v15);
    v25 = -1;
    sub_B52DAE(&v18);
  }
  else
  {
    AfxMessageBox(L"nono..", 0, 0);
  }
  return (*(int (**)(void))(*(_DWORD *)v1 + 344))();
}
```

이런저런 변수들이 좀 많긴 한데, 대충 35라인 정도에 break point를 걸고 debugging을 시도해 보았다.

![img]({{page.rpath|prepend:site.baseurl}}/debug.png)

eax(v3)와 esi(v4)의 값을 찾아 확인해 보면 내가 입력한 값과 길이가 있는 것을 알 수 있다.

그 아래로는 if문들이 있는데, 세 번의 if문에서 true 조건을 한 번이라도 만족하면 v2는 0이되고, 4번째 if문에서 else 조건을 타서 "nono.."라는 문자열을 출력하게 되는 것을 알 수 있다.

첫 번째 if 문에서 입력의 길이가 12보다 길어야 하는걸 알 수 있고, 두 번째와 네 번째 if문에서는 각각 "_my_b"와 "birth"라는 문자열이 포함되어야 한다는걸 알 수 있다. 세 번째 if문에서는 문자열이 "1114"로 시작하는지를 확인하고, 다섯 번째 if문에서는 길이를 14보다 작도록 제한하고 있으므로, 이 조건들을 감안하면 필요한 입력값은 "1114_my_birth"임을 알 수 있다.

실행파일을 다시 실행 시켜서 찾아낸 값을 넣으면 "GOOd!"이라는 칭찬과 함께 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **7670c30aca4606e5f4585935c3e2cf2aa46c078c**
