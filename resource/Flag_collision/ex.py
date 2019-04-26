from pwn import *
import hashlib
import itertools
import crc

def findhash(f, s, e, t):
	c = 0
	while True:
		digest = f(str(c)).hexdigest()
		if digest[s:e] == t:
			print str(c)
			return str(c)
		c += 1

r = remote("37.139.9.232", 19199)

m = r.recvline()
print m

#check PoW
if m.startswith("Submit a printable string X, such that "):
	m = m[39:]
	h = m.split("(X)")[0]
	pair = m.split("[")[1].split("]")[0].split(":")
	s, e = map(int, pair) if len(pair[1]) > 0 else int(pair[0]), None
	target = m.split(" = ")[1].strip()
	print h, s, e, target
	h_inst = eval("hashlib." + h)
	msg = findhash(h_inst, s, e, target)
	r.sendline(msg)

r.interactive()

m = r.readline()
while True:
	print r.recvuntil("len = ")
	m = r.recvline()
	print m

	l = m.split()[0]
	r.sendline(crc.get_crc_pair(int(l)))

	m = r.readline()
	if "next level" not in m:
		break

print m

r.close()
