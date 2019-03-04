#Hey, you're a hacker, right? I think I am too, look at what I made!  (2531257, 43) 
# My super secret message: 906851 991083 1780304 2380434 438490 356019 921472 822283 817856 556932 2102538 2501908 2211404 991083 1562919 38268  
#Problem is, I don't remember how to decrypt it... could you help me out?  Difficulty: easy

import gmpy2

n = 2531257
e = 43

msg = map(int, "906851 991083 1780304 2380434 438490 356019 921472 822283 817856 556932 2102538 2501908 2211404 991083 1562919 38268".split())

#print msg

for i in xrange(2, n / 2):
	if n % i == 0:
		p = i
		break

q = n // p
print (p, q)

assert n == p * q

phi_n = (p - 1) * (q - 1)

d = gmpy2.powmod(e, -1, phi_n)

assert gmpy2.powmod(e * d, 1, phi_n) == 1

d = [(int(gmpy2.powmod(m, d, n))) for m in msg]

print d

s = "".join(["%d"%i for i in d])
print s

r = ""
t = ""
for c in s:
	t += c
	if int(t) > 31 and int(t) < 128:
		r += chr(int(t))
		t = ""

print r
