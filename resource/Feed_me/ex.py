from pwn import *

'''
v6, v7, v8 : random

v9 + v10 = v6
v10 + v11 = v7
v11 + v9 = v8

v9 - v11 = v6 - v7

v9 = (v6 - v7 + v8) / 2
v10 = v6 - v9
v11 = v8 - v9
'''

#r = process("./challenge1")
r = remote("159.89.166.12", 9800)

r.recvuntil(":)\n")
m = r.recvline()
print m
m = [int(s.strip()) for s in m.split(';')[:3]]
print m

v6, v7, v8 = m[0], m[1], m[2]

v9 = (v6 - v7 + v8) / 2
v10 = v6 - v9
v11 = v8 - v9

payload = "%010d"%(v9)
payload += "%010d"%(v10)
payload += "%010d"%(v11)
r.sendline(payload)

r.interactive()

r.close()
