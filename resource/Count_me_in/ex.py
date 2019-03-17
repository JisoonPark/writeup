def chunk(input_data, size):
    return [input_data[i:i + size] for i in range(0, len(input_data), size)]


def xor(*t):
    from functools import reduce
    from operator import xor
    return [reduce(xor, x, 0) for x in zip(*t)]

def xor_string(t1, t2):
    t1 = map(ord, t1)
    t2 = map(ord, t2)
    return "".join(map(chr, xor(t1, t2)))

def depad(s):
    cnt = ord(s[-1])
    if cnt > 16:
        return s

    if s.endswith(s[-1] * cnt):
        return s[:-cnt]
    return s

plaintext = """The Song of the Count

You know that I am called the Count
Because I really love to count
I could sit and count all day
Sometimes I get carried away
I count slowly, slowly, slowly getting faster
Once I've started counting it's really hard to stop
Faster, faster. It is so exciting!
I could count forever, count until I drop
1! 2! 3! 4!
1-2-3-4, 1-2-3-4,
1-2, i love couning whatever the ammount haha!
1-2-3-4, heyyayayay heyayayay that's the sound of the count
I count the spiders on the wall...
I count the cobwebs in the hall...
I count the candles on the shelf...
When I'm alone, I count myself!
I count slowly, slowly, slowly getting faster
Once I've started counting it's really hard to stop
Faster, faster. It is so exciting!
I could count forever, count until I drop
1! 2! 3! 4!
1-2-3-4, 1-2-3-4, 1,
2 I love counting whatever the
ammount! 1-2-3-4 heyayayay heayayay 1-2-3-4
That's the song of the Count!
"""

ct = open("output.txt").read().decode("hex")

res = chunk(xor_string(plaintext, ct[:len(plaintext)]), 16)

s = set(res)

print ("#blocks", len(res))
print ("#unique blocks", len(s))

import string

for ctb in chunk(ct[len(plaintext):], 16):
    for ks in s:
        res = depad(xor_string(ks, ctb))
        if reduce(lambda a,b: a and (b in string.printable), [True] + list(res)):
            print res
    print ""

