from Crypto.PublicKey import RSA
from gmpy2 import iroot
from Crypto.Util.number import *

keypair_pem = open("publickey.pem", "r").read()
keypair = RSA.importKey(keypair_pem)

ct = open("flag.encrypted", "rb").read()

t = 4 * keypair.e * keypair.n
for k in range(1, 1000000):
  (y, b) = iroot(1 + t * k, 2)
  if b and (1 + y) % (keypair.e * 2) == 0:
    print k
    q = (1 + y) // (keypair.e * 2)
    break

p = keypair.n // q
piN = (p - 1) * (q - 1)

d = inverse(keypair.e, piN)

'''
pt = pow(bytes_to_long(ct), d, keypair.n)
print long_to_bytes(pt)
'''
#same as above
priv = RSA.construct((keypair.n, keypair.e, long(d)))
print priv.decrypt(ct)

#RSAES-PKCS1_v1_5 padding example
from Crypto.Cipher import PKCS1_v1_5
cipher = PKCS1_v1_5.new(priv)
print cipher.decrypt(ct, 0)
