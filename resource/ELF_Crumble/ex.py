from pwn import *
import itertools

prologue = asm("push ebp; mov ebp, esp")
ret = asm("ret")

fragments = ["fragment_%d.dat"%i for i in range(1, 9)]
data = [(fn, open(fn).read()) for fn in fragments]

#find first, last, and residuals
first = ""
last = ""
s = []
l = 0
for fn, d in data:
	l += len(d)
	if d.startswith(prologue):
		print "first : " + fn
		first = d
		continue
	if d.endswith(ret):
		print "last : " + fn
		last = d
		continue

	s.append(d)

funcs = ["f1", "f2", "f3", "recover_flag", "main"]
e = ELF("./broken")
locs = [e.symbols[f] for f in funcs]
e.write(locs[0], first)
e.write(locs[0] + l - len(last), last)
loc = locs[0] + len(first)

for t in itertools.permutations(s):
	e.write(loc, "".join(t))

	success = True
	for i in locs[1:]:
		if e.read(i - 1, len(ret)) != ret:
			success = False
			break

	if success:
		e.save()
		p = e.process()
		print p.recv()
		p.close()
