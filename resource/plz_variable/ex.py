from pwn import *
import z3
import re

r = remote("wargame.kr", 10004)

for idx in range(30):
	print "====================="
	print r.recvuntil("th...\n")
	print "=====================\n"

	eqs = r.recvuntil("-> ")
	print eqs

	eqs = [l.replace("=", "==") for l in eqs.split("\n")[:-1]]

	'''
	variables = set()
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	for c in alphabet:
		for l in eqs:
			if c in l:
				variables.add(c)
				break

	variables = list(variables)
	'''
	#same as above
	variables = list(set(re.findall(r"[a-z]","".join(eqs))))
	variables.sort()

	solver = z3.Solver()

	#add variables and their ranges
	for var in variables:
		exec("%c = z3.Int('%c')"%(var,var))
		solver.add(eval("%s >= 100"%var))
		solver.add(eval("%s <= 1000"%var))

	#add equations
	for eq in eqs:
		solver.add(eval(eq))

	#solve!
	solver.check()
	ans = solver.model()

	print ans

	#get response, there's no zip API
	resp = []
	for var in variables:
		resp.append(str(ans.evaluate(eval(var)).as_long()))

	r.sendline(",".join(resp))

r.interactive()
r.close()
