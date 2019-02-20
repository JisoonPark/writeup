---
layout: post
title: wanna_smile
category: Forensic
rpath: /resource/wanna_smile
tag: [ransomeware, openssl] 
---

**Category:** Forensic

**Source:** HDCON 2017 Quals(September)

**Points:** 200

**Author:** Jisoon Park(js00n.park)

**Description:** 

> 랜섬웨어를 분석하여 암호화된 문서를 복호화하고 플래그를 찾으시오.
>
>!!!!리얼머신이 아닌 가상머신에서 분석해야 하며 실행시키면 안됩니다. !!!!
>
>!!!!두번 실행시키면 복구가 불가능하오니 이점 양해해주십시오.!!!!!

## Write-up

문제 파일을 열어서 복호화 해보면, 최종적으로 decrypt 해야 할 파일과 악성코드로 보이는 실행파일, 그리고 덤프파일(아마 메모리 덤프)이 존재한다.

![img]({{page.rpath|prepend:site.baseurl}}/files.png)

암호화된 파일은 지금 열어봐야 아무런 도움이 안될테니, 실행파일과 덤프 파일 중에서 우선 덤프 파일을 확인해 보자.  
240MB가 넘는 큰 파일이 때문에, 한땀한땀 보기 보다는 strings 명령어를 이용해서 10글자 이상의 문자열들만 먼저 찾아본다.

```
$ strings -n 10 wanna_samile.exe.dmp > wanna_smile.exe.dmp.strings
```

찾아진 문자열들을 확인해나가다 보면... 응? Public Key가 보인다.

![img]({{page.rpath|prepend:site.baseurl}}/public_key.png)

밑져야 본전이니 PRIVATE 문자열을 검색해보자.

![img]({{page.rpath|prepend:site.baseurl}}/private_key.png)

맙소사.. 일단 복사해서 소중히 간직해 두기로 한다. 개인적인 생각이지만, 출제자가 일부러 넣어둔게 아닌것 같다는 생각을 했다. search 해보면 알겠지만, 이 부분 말고 Private Key가 일부만 들어있는 문자열도 있다. 원래는 그쪽에서 Private Key를 복구해내야 하는 문제가 아니었을까... 어쨌든, 원래 400점이었던 이 문제의 배점이 대회 중에 200점으로 쪼그라들었다. ㅋ


Key Pair 확보로 든든해진 마음을 갖고 주어진 실행파일을 (실행은 하지 말라고 했으니) ida로 분석해본다.

찬찬히 뜯어보다 보면, 파일에 대한 암호화를 실행하는 sub_402960() 함수를 찾을 수 있다. 위아래로 이런저런 코드들이 있지만, 실제로 봐야 할 부분은 얼마 안된다. 다행히 코드를 꼬아놓거나 하진 않았다.

![img]({{page.rpath|prepend:site.baseurl}}/encrypt_file.png)

위 코드를 살펴보자. sub_401080() 함수는 256bit AES Key를 세팅하는 함수이고, sub_4010D0() 함수는 AES Key를 이용해서 원래의 파일을 암호화 하는 함수이다. sub_402220() 함수에서 AES Key를 RSA로 암호화 하고, sub_4028C0() 함수에서 최종적으로 암호화된 파일을 완성한다.

![img]({{page.rpath|prepend:site.baseurl}}/file_write.png)

sub_2028C0() 함수를 조금 더 살펴보면, decryptme.docx.smile 파일의 헤더 구조를 확인할 수 있다. 아래와 같이, "WANASML!" 문자열로 시작하고 12번째 바이트에서부터 암호화된 AES Key가 기록되며, 272번째 바이트에서 원래 파일의 길이가 기록된다.

![img]({{page.rpath|prepend:site.baseurl}}/decryptme_header.png)

AES Key를 복호화해내기 위한 RSA Private Key는 알고 있으니, decryptme.docx.smile 파일로부터 암호화된 AES Key 부분을 조심스럽게 추출해낸다.

![img]({{page.rpath|prepend:site.baseurl}}/decryptme_encrypted_aes_key.png)

별도의 python 스크립트, Java 또는 C 코드를 작성해도 무방하나, 간단히 사용할 수 있는 openssl command line tool을 사용해보자.

![img]({{page.rpath|prepend:site.baseurl}}/decrypt_rsa.png)

별다른 에러 메세지가 없는 걸로 봐서 성공적으로 복호화가 된것 같은데, 복호화된 파일의 크기가 245바이트이다. 정상적인 AES 256 Key라면 32 바이트이어야 할텐데, 크기가 이상하니, ida에서 AES Key를 암호화 하는 부분을 잠깐 살펴본다.

![img]({{page.rpath|prepend:site.baseurl}}/encrypt_key.png)

입력받은 AES Key의 길이는 32 바이트가 맞는데, 실제로 RSA_public_encrypt() 함수를 호출하면서 암호화 할 길이(v8)로 245 바이트를 지정하고 있다. 이걸로 미루어, RSA 복호화는 정상적으로 수행되었고, 복호화 된 245 바이트 중 첫 32 바이트가 AES Key임을 알 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/aes_key.png)

openssl command line tool을 한번 더 사용하여 decryptme.docx.smile을 파일을 복호화 하자.(헤더 부분 제외)

![img]({{page.rpath|prepend:site.baseurl}}/aes_decrypt.png)

헤더의 마지막에 0x6517 바이트로 원본의 길이가 기록되어 있었으니, 길이에 맞게 파일을 잘라주자. (잘라주지 않아도 큰 상관은 없다. 보통 파일 뒤의 부가 정보는 크게 문제가 되지 않으므로) 다만, AES Key를 암호화 할 때 PKCS 패딩을 한게 아니기 때문에, 그냥 복호화 하면 openssl이 에러를 출력한다. 그래서 -nopad 옵션을 주고 패딩을 계산하지 않도록 해야 정상적인 복호화가 가능하다.

파일 이름에도 docx라고 나와있었지만, 확인 결과 Microsoft Word 파일이므로 docx로 확장자를 변경하고 파일을 열어보면 flag를 획득할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **TIMEISGOLD!**
