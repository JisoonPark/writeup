import gmpy2
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

g = 10
p =      0x13862420eba6fc60ee4d0d85ca7ab02705bb17da22a8ecb43f20208f08cf9b6b3d34cd6a8f14650a7c1
pubA =    0xe58b9d1d41dfc8c82984e8bd6f06148c74d651a0e1fc51ddbed14a9c4918ad2826201a5ca70e3c89cb
pubB =    0xb95280ad174b58689cafba85ad968a7448d7074dafbf5fb319495380e8d444275ad2f952e7cfffc84b
enc_key = 0x639d0641f794654b0e7f30b17bca3cafb4fa8b87d514485816eabffdd8c29f5b91ccea9a4ba4e2d8f9

cipher = "\x8d\xaa\x19\x2c\x19\xdc\x40\x37\xb5\x8d\xef\x29\x35\x62\x37\x04\x85\x67\x79\xce\xfe\x83\xff\x90\x42\x67\x7b\x9b\x62\x66\x1c\x59"

privA = 333623895364814584400934325632016654841259729259576270868893933041709102871414502757155867187502100
privB = 68366528803802774494102028092185614536187281887082630883946649435775005432542

'''
F = GF(p)
g = F(10)
b = F(pubA)
N = p-1

qi = [p^N.valuation(p) for p in prime_factors(N)]
l = len(qi)
Nqi = [ N/q for q in qi ]
ai = [g^r for r in Nqi ]
bi = [b^r for r in Nqi ]
xi = [ discrete_log(bi[i],ai[i]) for i in range(l) ]
x = CRT(xi,qi)
'''

assert((gmpy2.powmod(g, privA, p) == pubA) and (gmpy2.powmod(g, privB, p) == pubB))

shared_secret = gmpy2.powmod(pubA, privB, p)
print shared_secret

k = gmpy2.invert(shared_secret, p)
k = long_to_bytes((k * enc_key) % p)

aes = AES.new(k, AES.MODE_ECB)
print aes.decrypt(cipher)
