import requests
import base64
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
from Crypto.Cipher import AES
import zlib
import sys

#refer to PGP ASCII ARMOR and Raidx-64(https://tools.ietf.org/html/rfc4880#section-6.2)
def getPackets(m):
	m = m.split("\n")
	f = 0
	r = ""
	for l in m:
		if len(l) == 0:
			f = 1
			continue
		if (f == 0): continue
		if l[0] == "=": break

		r = r + l

	return base64.b64decode(r)

def getCompressedLength(msg):
	url = "http://drinks.teaser.insomnihack.ch/generateEncryptedVoucher"

	data = {"recipientName" : msg, "drink" : "beer"}
	headers = {"Content-type" : "application/json"}

	resp = requests.post(url, json=data, headers=headers)
	m = getPackets(resp.text)
	return ord(m[16])

#refer to https://www.rogdham.net/2018/09/17/csaw-ctf-2018-write-ups.en
def solve(oracle, suffix, charset):
	out = []
	for c in charset:
		#data = c + suffix
		data = suffix + c
		data *= 5
		while len(data) < 20:
			data = '<' + data  # pad  
		out.append((c, oracle(data)))
	max_value = max(out, key=lambda o: o[1])[1]
	return [o[0] for o in out if o[1] != max_value]

def solve_all(oracle):
	suffixes = ['||']
	charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-|!@#$*.,?/=\\ "
	while suffixes:
		new_suffixes = []
		for suffix in suffixes:
			if suffix:
				# skip loops at the right of suffix
				if suffix.endswith(suffix[-1:] * 3):
					continue
				if suffix.endswith(suffix[-2:] * 3):
					continue
			chars = solve(oracle, suffix, charset)
			if not(chars):
				yield suffix
				continue
			for char in chars:
				#new_suffixes.append(char + suffix)
				new_suffixes.append(suffix + char)
		print suffixes
		suffixes = new_suffixes

for solved in solve_all(getCompressedLength):
	print solved





'''
print "###############"
print "# Failed Try  #"
print "###############"
#refer to https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-09-14-CSAW-CTF-Quals/scripts/flatcrypt.py
#padding = b"1234567890ABCDEFGHIJ"
padding =  b"abcdefghijklmnopqrst"
known_flag = b"||G1MME_B33R_PLZ_1MM_S0_V3RY_TH1RSTY"
alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-|!@#$*.<>,?/=\\ "

while True:
	bestCandidate = None
	bestLen = 10000
	worstLen = -1

	for candidate in alphabet:
		check = padding + known_flag + candidate + padding

		resultLen = getCompressedLength(check)

		# update best and worst results
		if resultLen < bestLen:
			bestLen = resultLen
			bestCandidate = candidate
		worstLen = max(worstLen, resultLen)

		sys.stdout.write('.')
		sys.stdout.flush()

	if worstLen == bestLen:
		print "done!"
		break

	known_flag = known_flag + bestCandidate
	print known_flag

#'''
'''
url = "http://drinks.teaser.insomnihack.ch/generateEncryptedVoucher"

data = {"recipientName" : "matta", "drink" : "beer"}
headers = {"Content-type" : "application/json"}

voucher = (requests.post(url, json=data, headers=headers)).text

print voucher

url = "http://drinks.teaser.insomnihack.ch/redeemEncryptedVoucher"

data = {"encryptedVoucher" : voucher, "passphrase" : known_flag[2:]}
headers = {"Content-type" : "application/json"}

resp = requests.post(url, json=data, headers=headers)

print resp.text
'''
