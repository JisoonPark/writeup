funcs = open("functions").read().split("__int64 __fastcall ")[1:]
funcs = [0 if "^" in s.split("\n")[2] else 1 for s in funcs]

checkFlag = open("checkFlag").read().split("(unsigned int)")[1:]

r = dict()
cnt = 0
for s in checkFlag:
	t  = s.split("a1")[1].split(" ")
	idx, sh = 0, 0
	if t[0].startswith("["):
		idx = int(t[0][1:-1])
	if t[1] == ">>":
		sh = int(t[2][:-1])

	if idx in r:
		r[idx] += ((1 ^ funcs[cnt]) << sh)
	else:
		r[idx] = ((1 ^ funcs[cnt]) << sh)

	cnt += 1

print "".join([chr(r[i]) for i in range(832 / 8)])
