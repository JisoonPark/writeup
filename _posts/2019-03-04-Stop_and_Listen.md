---
layout: post
title: Stop and Listen
category: Web
source: "TAMUctf 2019"
rpath: /resource/Stop_and_Listen
tag: [openvpn, wireshark]
---

**Category**: Web/Network

**Source**: TAMUctf 2019

**Points**: 348

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Sometimes you just need to stop and listen.
> 
> This challenge is an introduction to our network exploit challenges, which are hosted over OpenVPN.
> 
> [Instructions](https://gist.github.com/nategraf/74204dd8b55fb20d29c32ae2bb2ff679):
  * Install OpenVPN. Make sure to install the TAP driver.
    * Debian (Ubuntu/Kali) linux CLI: apt install openvpn
    * [Windows GUI installer](https://openvpn.net/community-downloads/)
  * Obtain your OpenVPN configuration in the challenge modal.
    * You will obtain a separate config for each challenge containing connection info and certificates for authentication.
  * Launch OpenVPN:
    * CLI: sudo openvpn --config ${challenge}.ovpn
    * Windows GUI: Place the config file in %HOMEPATH%\OpenVPN\config and right-click the VPN icon on the status bar, then select the config for this challenge
> 
> The virtual tap0 interface will be assigned the IP address 172.30.0.14/28 by default. If multiple team members connect you will need to choose a unique IP for both.
> 
> The standard subnet is 172.30.0.0/28, so give that a scan ;)
> 
> If you have any issues, please let me (nategraf) know in the Discord chat
> 
> Some tools to get started:
  * [Wireshark](https://www.wireshark.org/)
  * [tcpdump](http://man7.org/linux/man-pages/man1/tcpdump.1.html)
  * [nmap](https://nmap.org/)
  * [ettercap](http://www.ettercap-project.org/ettercap/)
  * [bettercap](https://github.com/bettercap/bettercap/)
> 
> [OpenVPN Config]({{site.github.master}}{{page.rpath}}/listen.ovpn)

## Write-up

일단 OpenVPN을 이용해서 VPN에 접속하자. VPN에 접속하는 방법은 나같은 newbie들을 위해 문제에서 자세히 알려준 방법을 참고했다. (안내에는 TAP driver를 설치하라고 나와 있는데, Ubuntu 18.04에는 별도로 설치하지 않아도 VPN 접속에 문제가 없었다.)

VPN 접속 후 ifconfig를 해보면 내 IP는 172.30.0.14인 것을 알 수 있다. 문제에서 알려준 것은 여기까지. 이후로는 스스로 찾아봐야 한다.

일단 접속 가능한 서버가 뭐가 있을지 찾기 위해 IP Scanning을 해보자.

![img]({{page.rpath|prepend:site.baseurl}}/ipscan.png)

나(172.30.0.14) 외에 **172.30.0.2** 서버가 존재하는 것을 알 수 있다.

해당 서버에 어떤 포트가 열려있는지 알기 위해 nmap(zenmap)을 이용해 Port Scanning을 해보자.

![img]({{page.rpath|prepend:site.baseurl}}/portscan.png)

열려있는 포트가 없다.

아무리 뒤져봐도 다른 IP나 열려있는 포트를 찾지 못했다. 한참을 고민하다가, wireshark를 이용하여 tap0 인터페이스를 관찰했더니 **172.30.0.2** PC가 **172.30.0.15**번으로 UDP 패킷을 계속 날리는 것을 볼 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/wireshark.png)

해당 UDP Packet들을 follow 한 결과, 중간에 flag로 보이는 것을 발견하여 submit 하였다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **gigem{f0rty_tw0_c9d950b61ea83}**
