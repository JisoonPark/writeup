#!/usr/bin/env python3

import pickle
import gmpy2
from rusad import *

f = open("key.sad.pub", "rb")
key = pickle.load(f)

assert(isinstance(key, Key))

'''
print(key.bits)
print(key.E)
print(key.N)
print(key.iPmQ)
print(key.iQmP)
'''

i1 = key.iPmQ
i2 = key.iQmP

#i1*p^2 - (1 + n)*p + i2n = 0
#(-b +- root(b^2 - 4ac)) / 2a
a = i1
b = -(1 + key.N)
c = i2 * key.N
inner = b**2 - 4*a*c
assert(inner >= 0)

y, issquare = gmpy2.iroot(inner, 2)
assert (issquare)

x = [-b + y, -b - y]
p = list(filter(lambda x: x > 0 and x % (2*a) == 0, x))
assert(len(p) == 1)

p = p[0] // (2 * a)
q = key.N // p
assert(p * q == key.N)

phiN = (p - 1) * (q - 1)
d = gmpy2.invert(key.E, phiN)

key.P = p
key.Q = q
key.D = d
key.DmP1 = d%(p - 1)
key.DmQ1 = d%(q - 1)

data = open("flag.enc", "rb").read()
print(decrypt(key, data))
