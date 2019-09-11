from pwn import *
from Crypto.Util.number import long_to_bytes

r = remote("68.183.158.95", 7777)

r.recvuntil(" --- ")
c = int(r.readline().strip())		#c = pow(flag, e, n)

r.sendlineafter("Exit\n", "1")		#encrypt
r.sendlineafter("\n", "\x02")

cp = int(r.readline().strip())		#cp = pow(2, e, n)
#print "cp", cp

r.sendlineafter("Exit\n", "2")		#decrypt

r.sendlineafter("\n", str(c * cp))

p = int(r.readline().strip())		#p = pow(pow(flag, e, n) * pow(2, e, n), d, n) = 2 * flag

p = p / 2

print long_to_bytes(p)

r.close()

