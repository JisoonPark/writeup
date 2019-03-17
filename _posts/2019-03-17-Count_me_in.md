---
layout: post
title: Count me in
category: Crypto
source: "CONFidence CTF 2019 Teaser"
rpath: /resource/Count_me_in
tag: [CTR, multiprocessing]
---

**Category**: Crypto

**Source**: CONFidence CTF 2019 Teaser

**Points**: 59

**Author**: Jisoon Park(js00n.park)

**Description:** 

> I've been lately using this cool AES-CTR, but it was super slow, so I made a parallel version. Now it's blazing fast, but for some reason I have trouble decrypting the data...
> 
> [count_me_in.tar.gz]({{site.github.master}}{{page.rpath}}/count_me_in.tar.gz)

## Write-up

암호화 코드와 암호화된 데이터가 주어진다.

먼저 암호화 코드를 살펴보자.

```python
def worker_function(block):
    global counter
    key_stream = aes.encrypt(pad(str(counter)))
    result = xor_string(block, key_stream)
    counter += 1
    return result


def distribute_work(worker, data_list, processes=8):
    pool = multiprocessing.Pool(processes=processes)
    result = pool.map(worker, data_list)
    pool.close()
    return result


def encrypt_parallel(plaintext, workers_number):
    chunks = chunk(pad(plaintext), 16)
    results = distribute_work(worker_function, chunks, workers_number)
    return "".join(results)


def main():
    plaintext = """The Song of the Count

You know that I am called the Count
Because I really love to count
I could sit and count all day

[...]

""" + flag
    encrypted = encrypt_parallel(plaintext, 32)
    print(encrypted.encode("hex"))
```

평문의 일부가 주어져 있고, 평문을 16바이트 단위로 쪼개서 32개의 프로세스로 나누어 암호화를 하고 있다.

딱 보면 worker_function()에서 global counter를 사용하는데, multiprocess 환경에서 global 변수 사용에 대한 아무런 대비가 되어있지 않다.

어떤 일이 일어날 수 있을까. 아마 **counter += 1**이 제대로 반영되지 않아서 동일한 counter 값들이 사용될 수 있을 것 같다. key는 공통이니 counter가 동일하면 keystream도 동일한 것들이 있을 것이다. 진짜 그런지 살펴보자.

CTR 모드를 구현했는데, 평문을 알고 있으니 암호문과 xor 하여 key stream을 구할 수 있다. 전체 keystream의 갯수를 세어 보면 총 57개인데, 이 중에 중복을 제거해 보면 8개 keystream 밖에 남지 않는다. counter는 0부터 7까지만 사용되었다는 의미이다.

8개의 key stream을 이용해서 암호문 중 평문이 알려지지 않은 부분을 복구해보자. 암호문의 각 block을 8가지 key stream과 xor 하면서 padding이 되어있거나 printable한 문자들로만 이루어진 것들을 찾아 모으도록 [exploit]({{site.github.master}}{{page.rpath}}/ex.py)을 작성하였더니 flag를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **p4{at_the_end_of_the_day_you_can_only_count_on_yourself}**
