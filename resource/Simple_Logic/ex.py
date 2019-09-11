ROUNDS = 765
BITS = 128

Pair = [(0x29abc13947b5373b86a1dc1d423807a, 0xb36b6b62a7e685bd1158744662c5d04a),
	(0xeeb83b72d3336a80a853bf9c61d6f254, 0x614d86b5b6653cdc8f33368c41e99254),
	(0x7a0e5ffc7208f978b81475201fbeb3a0, 0x292a7ff7f12b4e21db00e593246be5a0),
	(0xc464714f5cdce458f32608f8b5e2002e, 0x64f930da37d494c634fa22a609342ffe),
	(0xf944aaccf6779a65e8ba74795da3c41d, 0xaa3825e62d053fb0eb8e7e2621dabfe7),
	(0x552682756304d662fa18e624b09b2ac5, 0xf2ffdf4beb933681844c70190ecf60bf)]

def encrypt(msg, key, mask):
    enc = msg
    for _ in range(ROUNDS):
        enc = (enc + key) & mask
        enc = enc ^ key
    return enc

def decrypt(msg, key):
    enc = msg
    mask = (1 << BITS) - 1
    for _ in range(ROUNDS):
        enc = enc ^ key
        enc = (enc - key) & mask
    return enc

def tryKey(idx, k):
	bits = (idx + 1) * 8
	mask = (1 << bits) - 1

	#termination condition
	if idx == 16:
		print "The flag: TWCTF{%x}" % decrypt(0x43713622de24d04b9c05395bb753d437, k)
                print "  ... from key", k
		return

	s = set()
	for n, (plain, enc) in enumerate(Pair):
		p = plain & mask

		c = set()
		for i in range(256):
			key = (i << (idx * 8)) + k
			if encrypt(p, key, mask) == enc & mask:
				c.add(key)
		#print c
		if n == 0:
			s |= c
		else:
			s &= c
	#print "candidates:", idx, hex(k), s

	for i in s:
		tryKey(idx + 1, i)

tryKey(0, 0)
