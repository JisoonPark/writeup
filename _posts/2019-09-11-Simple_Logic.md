---
layout: post
title: Simple Logic
category: Crypto
source: "TokyoWesterns CTF 5th 2019"
rpath: /resource/Simple_Logic
tag: [brute_force]
---

**Category**: Crypto

**Source**: TokyoWesterns CTF 5th 2019

**Points**: 103

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Simple cipher is always strong.
>
> Download: [simple_logic.7z]({{site.github.master}}{{page.rpath}}/simple_logic.7z)

## Write-up

압축을 풀어보면 encrypt.rb와 output 파일을 찾을 수 있다.

output 파일에는 암호화된 flag와 plaintext, ciphertext 쌍 6개가 주어져 있다.

ruby 코드도 살펴보자.

```ruby
[생략]

ROUNDS = 765
BITS = 128
PAIRS = 6

def encrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = (enc + key) & mask
        enc = enc ^ key
    end
    enc
end

[생략]

flag = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)
key = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)

STDERR.puts "The flag: TWCTF{%x}" % flag
STDERR.puts "Key=%x" % key
STDOUT.puts "Encrypted flag: %x" % encrypt(flag, key)
fail unless decrypt(encrypt(flag, key), key) == flag # Decryption Check

PAIRS.times do |i|
    plain = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)
    enc = encrypt(plain, key)
    STDOUT.puts "Pair %d: plain=%x enc=%x" % [-~i, plain, enc]
end
```

차사하게 flag와 Key는 빼고 줬나보다.

암호화 루틴을 보면 간단히 덧셈과 xor을 반복하는 것을 알 수 있다. 덧셈 연산을 하면 하위 바이트의 연산 결과에 상위 바이트가 영향을 받을 수 있으므로 하위 바이트부터 한 바이트씩 역산해가면 key를 복구 할 수 있을 것 같다.

주어진 샘플 암호문 중에서 하나를 골라 최하위 1 byte에 대해서 brute force를 시도하였더니 동일한 암호문을 만드는 key 값 여러 개를 찾을 수 있었다. 그래서 샘플을 하나가 아니라 6개를 준 것 같다.

최하위 byte 부터 각 pair에 대해 가능한 key의 조합을 뽑아서 교집합을 만들었더니 key 값을 찾을 수 있었고, 이를 이용하여 flag를 알아내었다. ([코드]({{site.github.master}}{{page.rpath}}/ex.py))

주어진 샘플값 모두를 만족시키는 key는 두 개를 찾을 수 있었는데, 이 중 어느 것을 사용하여도 동일한 flag를 얻을 수 있었다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag: **TWCTF{ade4850ad48b8d21fa7dae86b842466d}**
