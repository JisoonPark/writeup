---
layout: post
title: Snakes over cheese
category: Reversing
source: "TAMUctf 2019"
rpath: /resource/Snakes_over_cheese
tag: [pyc, decompile]
---

**Category**: Reversing

**Source**: TAMUctf 2019

**Points**: 370

**Author**: Jisoon Park(js00n.park)

**Description:** 

> What kind of file is this?
> 
> [reversing2.pyc]({{site.github.master}}{{page.rpath}}/reversing2.pyc)

## Write-up

pyc 파일이 주어졌다. pyc 파일은 디컴파일이 가능하다. 해보자.

```python
# Source Generated with Decompyle++
# File: reversing2.pyc (Python 2.7)

from datetime import datetime
Fqaa = [
    102,
    108,
    97,
    103,
    123,
    100,
    101,
    99,
    111,
    109,
    112,
    105,
    108,
    101,
    125]
XidT = [
    83,
    117,
    112,
    101,
    114,
    83,
    101,
    99,
    114,
    101,
    116,
    75,
    101,
    121]

def main():
    print 'Clock.exe'
    input = raw_input('>: ').strip()
    kUIl = ''
    for i in XidT:
        kUIl += chr(i)

    if input == kUIl:
        alYe = ''
        for i in Fqaa:
            alYe += chr(i)

        print alYe
    else:
        print datetime.now()

if __name__ == '__main__':
    main()
```

파일을 실행했을 때 입력한 값이 XidT 배열의 문자열과 같으면 Fqaa 배열을 보여준다.

Fqaa 배열의 내용을 확인해보자.

```
$ python -c 'import reversing2; print "".join(map(chr, reversing2.Fqaa))'
flag{decompile}
$
```

flag를 얻었다.

Flag : **flag{decompile}**
