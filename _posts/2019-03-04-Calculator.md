---
layout: post
title: Calculator
category: Web
source: "TAMUctf 2019"
rpath: /resource/Calculator
tag: [openvpn, ettercap, wireshark]
---

**Category**: Web/Network

**Source**: TAMUctf 2019

**Points**: 482

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Using a teletype network protocol from the 70s to access a calculator from the 70s? Far out!
> 
> Note to new players: You won't see anything in Wireshark / tcpdump when you initially connect. (i.e. packets are sent unicast on a bridged network)
> 
> [OpenVPN Config]({{site.github.master}}{{page.rpath}}/calculator.ovpn)

## Write-up

VPN에 접속한 다음 Wireshark로 tap0를 열어보자. 문제에서 얘기한 대로 별다른 패킷들이 보이지 않는다.

패킷들이 unicast로 날아다녀서 그런 거라고 하니 ettercap을 이용한 ARP spoofing을 통해 패킷을 살펴보자.

![img]({{page.rpath|prepend:site.baseurl}}/hosts.png)

먼저 ettercap을 실행하고, host 들을 scan 해보면 **172.30.0.2**와 **172.30.0.3** 두 개의 host가 찾아진다.

![img]({{page.rpath|prepend:site.baseurl}}/ettercap.png)

이들을 각각 Target 1과 Target 2로 지정한 다음, ARP poisoning - Sniff remote connections을 이용해서 sniffing을 시도하면 Target 1과 Target 2가 주고 받는 패킷들을 나도 볼 수 있게 된다.

(참고로, ettercap의 사용법은 [이 페이지](https://5log.tistory.com/96)에 잘 나와있다. 잘 정리되어있어서, 보고 따라해서 한번만에 성공했다.)

![img]({{page.rpath|prepend:site.baseurl}}/tap0.png)

wireshark를 이용해서 tap0 인터페이스에서 날아다니는 패킷들을 확인해보면, telnet 패킷들이 보인다. (문제에서 얘기한 **teletype network protocol**을 검색해보니 그게 telnet 프로토콜이라고 해서 바로 알았다.)

![img]({{page.rpath|prepend:site.baseurl}}/alice.png)

telnet 프로토콜의 패킷들을 follow 해보면 alice의 로그인 계정(alice / 58318008)을 확인할 수 있다.

Telnet host인 **172.30.0.2**에 alice의 계정으로 접속 후 디렉토리의 파일들을 살펴보면 **.ctf_flag** 파일이 있는 것을 볼 수 있고, flag를 알아낼 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/telnet.png)

Flag : **gigem{f5ae5f528ed5a9ad312f75bd1d3406a2}**
