import sys
import itertools

def getKeys(s4):
	z1, w1, z2, w2 = [ord(c) - 97 for c in s4]
	x1, y1, x2, y2 = [ord(c) - 97 for c in "pctf"]

	k0, k1 = [], []

	for k00 in range(10000):
		for k01 in range(10000):
			if ((x1 * k00 + y1 * k01)%26 == z1) and (x2 * k00 + y2 * k01)%26 == z2:
				k0 = [k00 % 26, k01 % 26]
				if len(k0) > 0 and len(k1) > 0: break
			if ((x1 * k00 + y1 * k01)%26 == w1) and (x2 * k00 + y2 * k01)%26 == w2:
				k1 = [k00 % 26, k01 % 26]
				if len(k0) > 0 and len(k1) > 0: break
		if len(k0) > 0 and len(k1) > 0: break

	return [k0, k1]

def encrypt(key, a, b):
	x = ord(a) - 97
	y = ord(b) - 97
	z = (x*key[0][0] + y*key[0][1])%26 + 97
	w = (x*key[1][0] + y*key[1][1])%26 + 97
	return chr(z) + chr(w)

def makedict(key):
	d = dict()
	alpha = "abcdefghijklmnopqrstuvwxyz"
	for a, b in itertools.product(alpha, repeat = 2):
		r = encrypt(key, a, b)
		d[r] = a + b
	return d

ciphertext = open("ciphertext.txt").read().strip()

for i in range(0, len(ciphertext), 2):
	try:
		key = getKeys(ciphertext[i:i + 4])
		d = makedict(key)

		flag = ""
		for j in range(i, len(ciphertext), 2):
			flag += d[ciphertext[j:j + 2]]
		print flag
	except:
		pass
