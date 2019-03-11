---
layout: post
title: ReadingRainbow
category: Web
source: "TAMUctf 2019"
rpath: /resource/ReadingRainbow
tag: [pcap, wireshark]
---

**Category**: Web

**Source**: TAMUctf 2019

**Author**: Jisoon Park(js00n.park)

----

## 0_Network_Enumeration

**Points:** 100

**Description:** 

> Recently, the office put up a private webserver to store important information about the newest research project for the company. This information was to be kept confidential, as it's release could mean a large loss for everyone in the office.
> 
> Just as the research was about to be published, a competing firm published information eerily similar. Too similar...
> 
> Time to take a look through the office network logs to figure out what happened.
> 
> 1. What is the IP address of the private webserver?
> 2. How many hosts made contact with the private webserver that day?
> 
> Difficulty: easy
>
> [capture.pcap]({{site.github.master}}{{page.rpath}}/capture.pcap)

### Write-up

PCAP 파일이 주어졌다. wireshark로 열어보자.

webserver라고 했으니 80번 포트로의 연결을 받아들이는 IP를 찾아보자.

![img]({{page.rpath|prepend:site.baseurl}}/server_ip.png)

거의 맨 위에 **192.168.11.4**가 나오는걸 알 수 있다. 넣어보니 맞다고 한다.

**ip.dst == 192.168.11.4** 필터를 적용한 후 Source IP를 세어보면 총 **13**개의 IP 주소를 확인할 수 있다.

1 : **192.168.11.4**  
2 : **13**

----

## 1_Discovery

**Points:** 100

**Description:** 

> 1. What is the IP address of the host exfiltrating data?
> 2. For how long did the exfiltration happen? (Round to the nearest second. Format: MM:SS)
> 3. What protocol/s was used to exfiltrate data? (Alphabetical order, all caps, comma separated, with spaces - ex: ABCD, BBCD)
> 
> Difficulty: easy

### Write-up

위에서 webserver에 접속하는 IP가 13개였었다. 순서대로 하나씩 넣어보면 **192.168.11.7**임을 알 수 있었다.

192.168.11.4와 192.168.11.7간의 통신 패킷들을 보면, 첫 패킷의 timestamp가 **14:24:40**이고, 마지막 패킷의 timestamp가 **14:35:49**이다. 두 시간을 빼보면 11분 9초임을 알 수 있다.

통신 프로토콜은 ICMP, TCP, HTTP, DNS의 네 가지를 이용하는데, 하나씩 살펴보면 SYN/ACK에만 사용되는 TCP 패킷을 제외하고 나머지 패킷들은 뭔가 데이터들을 들고 다니는 것을 확인할 수 있다.

1 : **192.168.11.7**  
2 : **11:09**  
3 : **DNS, ICMP, HTTP**

----

## 2_Exfiltration

**Points:** 100

**Description:** 

> 1. What is the name of the stolen file?
> 2. What is the md5sum of the stolen file?
> 
> Difficulty: easy

### Write-up

192.168.11.4와 192.168.11.7 간에 교환되는 패킷을 살펴보면, 맨 처음에 ICMP 패킷이 보인다.

Ping Request/Reply인데, 일반적인 Ping과는 다르게 Payload가 있다.

![img]({{page.rpath|prepend:site.baseurl}}/ping_payload.png)

이 값들을 decoding 해보자. 중간에 e라는 문자가 들어있는 걸로 봐서는 hex 데이터인것 같다.

디코딩 했더니 뭔가 읽을 수 있는 문자열이 나왔다. 딱 봐도 .(dot)은 field 구분자인 것 같다.

구분된 각각의 필드를 파일 이름으로 submit 해보았지만 아니었다. 중간에 있는 746f로 시작하는 데이터를 한번 더 디코딩 해보았더니 파일 이름같이 생긴 것이 나와서 넣어봤더니 정답이었다.

그렇다면 마지막에 있는 데이터는 16 바이트 길이인 것이 md5sum인 것 같다. submit 해보니 맞았다.

![img]({{page.rpath|prepend:site.baseurl}}/file_data.png)

1 : **totally_nothing.pdf**  
2 : **6156eab6691f32b8350c45b3fc4aadc1**

## 3_Data

**Points:** 100

**Description:** 

> 1. What compression encoding was used for the data?
> 2. What is the name and type of the decompressed file? (Format: NAME.TYPE e.g. tamuctf.txt)
> 
> Difficulty: medium-hard

### Write-up

DNS, ICMP, HTTP 프로토콜을 이용해서 전송되는 데이터들을 살펴보면, 각자의 방법으로 공통된 유형의 데이터를 보내고 있다.

![img]({{page.rpath|prepend:site.baseurl}}/http_data.png)

http 포로토콜은 POST payload를 이용해서 전송하고 있다.

![img]({{page.rpath|prepend:site.baseurl}}/icmp_data.png)

ICMP 프로토콜은 optional field인 message payload를 이용해서 전송한다.

![img]({{page.rpath|prepend:site.baseurl}}/dns_data.png)

DNS 프로토콜은 DNS query 메세지에 데이터를 실어보낸다.

wireshark로 각 프로토콜별로 메세지를 필터링하여 JSON 형태로 export 하였다.

각각의 프로토콜로 전송되는 메세지를 hex decode 해보면 SEx4IRV.__n__.__data__ 형식의 데이터를 획득할 수 있었다.

3가지 프로토콜로부터 총 51개의 데이터를 얻어내어 n으로 지정되는 순서에 따라 배치하고 hex decode를 한번 더 수행하는 [코드]({{site.github.master}}{{page.rpath}}/ex.py)를 작성한 결과 [file]({{site.github.master}}{{page.rpath}}/output)의 데이터를 얻을 수 있었다.

결과 file은 gzip 형식으로 압축되어 있었고, 이를 압축 해제하여 생성된 파일은 tar 파일이었다. (.tar.gz였다는 뜻)

tar를 풀어주자 최종적으로 stuff라는 elf 파일이 생성되었다.

![img]({{page.rpath|prepend:site.baseurl}}/output.png)

1 : **gzip**  
2 : **stuff.elf**
