#:100F4000982F9F7D9554933028F40C5F1F4FFFE33B


data = open("embedded_db.hex", "r").read().split('\r\n')[:-2]
totLen = 0
f = open("bin", "w")
for l in data:
	assert(l[0] == ":")
	dataLen = int(l[1: 3], 16)
	totLen += dataLen
	f.write(l[9: 9 + dataLen * 2].decode("hex"))

print totLen
