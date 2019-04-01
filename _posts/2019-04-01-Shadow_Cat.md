---
layout: post
title: Shadow Cat
category: Crypto
source: "VolgaCTF 2019 Qualifier"
rpath: /resource/Shadow_Cat
tag: [john_the_ripper]
---

**Category**: Crypto

**Source**: VolgaCTF 2019 Qualifier

**Points**: 100

**Author**: Jisoon Park(js00n.park)

**Description:** 

> We only know that one used /etc/shadow file to encrypt important message for us.
> 
> [shadow.txt]({{site.github.master}}{{page.rpath}}/shadow.txt) [encrypted.txt]({{site.github.master}}{{page.rpath}}/encrypted.txt)

## Write-up

shadow 파일(shadow.txt)과 암호화된 flag(encrypted.txt)가 주어진다.

dictionary를 이용해서 John the ripper로 shadow를 복호화 하려고 해봤지만 잘 되지 않았다.

shadow.txt에 a부터 z까지의 계정이 있고, 암호화된 flag가 소문자로만 이루어진 것이 치환암호인 것 같았다. 

```python
import itertools

a = "abcdefghijklmnopqrstuvwxyz"

f = open("dict.txt", "w")

for c in a:
        f.write(c + "\n")

for c in itertools.product(a, repeat=2):
        f.write("".join(c) + "\n")

for c in itertools.product(a, repeat=3):
        f.write("".join(c) + "\n")
```

한글자에서 많아야 세글자 정도가 flag 한글자일거라고 생각해서 소문자 1\~3글자가 조합된 dictionary를 새로 만들었다.

![img]({{page.rpath|prepend:site.baseurl}}/john.png)

이걸 이용했더니 shadow 파일을 성공적으로 복호화 할 수 있었다. ~~이럴거면 그냥 dictionary 파일을 만들지 말걸 그랬다.~~ 각 id와 복호화된 password를 이용해서 1:1 mapping table을 만들어서 암호하된 flag를 복호화 하였더니 아래와 같은 문자열을 얻을 수 있었다.

```
vaff_iafi_mpamxcns_iafimak_ayrahf_ybpxf_cn_kiq_fiajurf
```

혹시나 해서 submit 해보았으나 역시나 아니었다.

어떤걸 놓친 것일까 고민하다가 달리 할 수 있는게 없어서 mapping을 반복해서 시도해 보았다.

5번, 15번 했을 때는 별다른 의미있는 문자열을 얻지 못했지만 50번으로 늘려서 시도하자 의미있을 것 같은 문자열이 발견되었다.

```
pass_hash_cracoing_hashcab_always_lxros_in_bhe_shadkws
```

이정도면 우연히 만들어진 것을 아닌 것 같은데 알 수 없는 부분들이 있다. 특히 마지막은 '**shadow**'가 되어야 할 것 같은데 뭔가 완전하지 않다.

반복을 500번으로 늘리고 "pass"로 시작해서 "shadow"로 끝나는 문자열이 있는지 확인해 봤더니 의미있는 문자열이 출력되었다. ([코드]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

flag format에 맞게 제출했더니 point를 획득할 수 있었다.

Flag : **VolgaCTF{pass_hash_cracking_hashcat_always_lurks_in_the_shadows}**

