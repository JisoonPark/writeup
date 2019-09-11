cipher1 = '\x05F\x17\x12\x14\x18\x01\x0c\x0b4'
cipher2 = '>\x1f\x00\x14\n\x08\x07Q\n\x0e'

flagformat = "d4rk{}c0de"
r = ""
for i in range(10):
	r += chr(ord(cipher1[i]) ^ ord(cipher2[i]) ^ ord(flagformat[i]))

print "xor result is", r

print "flag is", flagformat[:5] + r[5:] + r[:5] + flagformat[5:]
