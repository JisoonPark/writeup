---
layout: post
title: pyc decompile
category: Reversing
rpath: /resource/pyc_decompile
tag: [pyc] 
---

**Category:** Reversing

**Source:** wargame.kr

**Points:** 353

**Author:** Jisoon Park(js00n.park)

**Description:** 

> bughela.pyc
> 
> :D

## Write-up

서버의 시간과 pyc 파일이 주어진다.

pyc 파일은 쉽게 decompile 할 수 있는데, 나는 pycdc라는 decompiler를 이용해서 다음과 같은 소스를 얻었다.


```python
import time
from sys import exit
from hashlib import sha512

def main():
    print 'import me :D'


def GIVE_ME_FLAG(flag):
    if flag[:43] != 'http://wargame.kr:8080/pyc_decompile/?flag=':
        die()
    flag = flag[43:]
    now = time.localtime(time.time())
    seed = time.strftime('%m/%d/HJEJSH', time.localtime())
    hs = sha512(seed).hexdigest()
    start = now.tm_hour % 3 + 1
    end = start * (now.tm_min % 30 + 10)
    ok = hs[start:end]
    if ok != flag:
        die()
    print 'GOOD!!!'


def die():
    print 'NOPE...'
    exit()

if __name__ == '__main__':
    main()
```

GIVE_ME_FLAG() 함수에 있는 내용을 복사해다가 'GOOD!!!'을 출력하는 flag를 만들면 될 것 같다.

```python
import time
from sys import exit
from hashlib import sha512
import requests

def make_flag():
    now = time.localtime(time.time())
    seed = time.strftime('%m/%d/HJEJSH', time.localtime())
    hs = sha512(seed).hexdigest()
    start = now.tm_hour % 3 + 1
    end = start * (now.tm_min % 30 + 10)
    ok = hs[start:end]
    return ok

URL = 'http://wargame.kr:8080/pyc_decompile'
data = {'flag' : make_flag()}

response = requests.get(URL, params = data)
print response.text
```

이대로 실행해보면 어찌된 일인지 WRONG......이라는 메세지가 나온다. 이게 왜이러나 싶어 유심히 보아도 별달리 틀린 부분을 못찾았는데, 서버 시간이 주어졌던게 생각나서 설마 하고 로컬 타임과 비교해 보았다.

```python
print "server time : " + response.headers['Date']
print "local time  : " + time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
```

```
server time : Fri, 21 Dec 2018 05:59:05 GMT
local time  : Fri, 21 Dec 2018 05:57:54 GMT
```

대충 1~2분 정도 빠르다. ㅡ_ㅡ;;


서버 시간을 받아서 파싱해도 되지만, 귀찮으니 11번 라인을 간단하게 고쳐서 사용했다.
```python
    end = start * ((now.tm_min + 2) % 30 + 10)
```

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **f17b0303b74c1c37e3be86b9461716074707b1b5**
