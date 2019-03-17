---
layout: post
title: Very Smooth
source: "SECCON 2017 Quals."
category: Crypto
rpath: /resource/Very_Smooth
tag: [RSA, factorization, pcap, wireshark] 
---

**Category:** Crypto

**Source:** SECCON 2017 Quals.

**Points:** 300

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Decrypt index.html from PCAP.
>
> Please, submit the flag in the format: "SECCON{" + Answer + "}"
>
>      Answer is written in index.html
>
> source : SECCON 2017 Quals.

## Write-up

파일의 압축을 풀어보면 pcap 파일 하나만 들어있다. 일단 wireshark로 열어보자

![img]({{page.rpath|prepend:site.baseurl}}/export_cert.png)

역시나 TLS 통신을 위한 패킷들이 보인다. 
살펴봐야 할 패킷 자체가 별로 없으므로, 한번 훑어보면 plain으로 주어진 힌트는 별달리 없는 것을 알 수 있다.

TLS 자체를 공격해야 할 것으로 생각되니, 우선 서버의 인증서를 추출하도록 한다.  
(위의 Wireshark 화면에서 Certificate 항목에서 우클릭 후 'Export packet bytes'를 하면 저장할 수 있다.)

![img]({{page.rpath|prepend:site.baseurl}}/cert_contents.png)

추출된 인증서를 열어보면 제대로 추출되어 정상적으로 파싱되는 것을 확인할 수 있다. 이제 인증서에서 서버의 공개키를 다시 추출한다.

![img]({{page.rpath|prepend:site.baseurl}}/extract_pubkey.png)

추출된 서버의 공개키에 대해 defactoring(인수분해)을 시도해본다. 당연히 해봐야 하는 시도이기도 하지만, 문제 이름에 'Smooth'가 들어가는 걸로 봐서 간단히 defactoring이 가능한 smooth number의 사용으로 인한 RSA 취약점 문제임을 유추할 수도 있다. (사실 나도 잘은 모른다......)

![img]({{page.rpath|prepend:site.baseurl}}/get_privatekey.png)

정확한 알고리즘은 모르지만(;;;) 빠른 시간 내에 defactoring에 성공하여 private key를 얻을 수 있다.

pcap 파일을 잘 보면 Key Exchange 후에 584번 포트를 이용해서 Application Data가 전송되는 것을 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/584.png)

얻어낸 private key를 이용하여 TLS 패킷을 복호화 해보자. 네트워크 패킷 분석 전문 도구인 wireshark는 IP와 포트를 이용해서 stream을 지정해주고 private key를 알려주면 알아서 TLS stream을 복호화 해준다.

![wiki]({{page.rpath|prepend:site.baseurl}}/wireshark_setting.png)

584번 포트의 데이터에 Follow -> SSL Stream을 적용하면 복호화된 html 컨텐츠를 확인할 수 있고, flag를 찾을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **SECCON{One of these primes is very smooth.}**
