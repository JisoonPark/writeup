from Crypto.PublicKey import RSA
from Crypto.Util.number import *
from gmpy2 import iroot, c_divmod, powmod, gcdext

keypair_pem = open("publickey.pem", "r").read()
keypair = RSA.importKey(keypair_pem)

n = keypair.n

#factor n
q, _ = iroot(n, 2)
while True:
	p, b = c_divmod(n, q)
	if b == 0:
		break
	q += 1

#get cipher text value
a = bytes_to_long(open("ciphertext.txt", "r").read().strip().decode("hex"))

#derypt rabin crypto
assert((p % 4 == 3) and (q % 4 == 3))
mp = powmod(a, (p + 1) // 4, p)
mq = powmod(a, (q + 1) // 4, q)

_, yp, yq = gcdext(p, q)
r = (yp * p * mq + yq * q * mp) % n
s = (yp * p * mq - yq * q * mp) % n

candidates = [r, n - r, s, n - s]

#rabin crypto returns 4 candidates, and the plain text should be one of them
print "\n\n".join(map(long_to_bytes, candidates))
