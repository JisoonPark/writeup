import md5

i = 0
while True:
	m = md5.new()
	m.update(str(i))
	if "'='" in m.digest():
		print str(i)
		print m.digest()
		break
	i = i + 1
