from pwn import *
from gmpy2 import gcd, powmod

r = remote("95.213.235.103", 8801)

r.readline()		#Hi, bro!
r.readline()		#Try this:

s = []
while True:
	m = r.readline()
	if m.startswith("Predict"):		#Predict next one!
		r.readuntil(">>>")			#>>>
		break
	s.append(int(m.strip()))

t = []
u = []
for i in range(len(s) - 1):
	#t[n] = s[n + 1] - s[n]
	t.append(s[i + 1] - s[i])

for i in range(len(t) - 2):
	#u[n] = abs(t[n + 2] * t[n] - t[n + 1]^2)
	u.append(abs(t[i + 2] * t[i] - t[i + 1] ** 2))

#p = GCD of u
p = reduce(gcd, u)

t0_inv = powmod(t[0], -1, p)
a = t[1] * t0_inv % p
b = (s[1] - a * s[0]) % p

print "p, a, b = ", p, a, b

nxt = (a * s[-1] + b) % p

r.sendline("%d"%nxt)
r.interactive()
