import requests
import base64
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
from Crypto.Cipher import AES
import zlib

#refer to Iterated and Salted S2K(https://tools.ietf.org/html/rfc4880#section-3.7.1.3)
#         and (http://rays-notebook.info/computing/crypto-gnupg-s2k.html#itersalted)
def getKey(passphrase, salt, cnt, keyLen):
	iterate = salt + passphrase
	niter = cnt / len(iterate) + 1

	m = hashlib.sha1()
	m.update((iterate * niter)[:cnt])
	r = m.digest()
	if (len(r) < keyLen):
		m = hashlib.sha1()
		m.update('\x00' + (iterate * niter)[:cnt])
		r = r + m.digest()

	return r[:keyLen]

#python CFB is working as CFB8 (as default)
#change CFB8 to CFB by using segment_size option.
#in this case, padding is necessary though we're using CFB mode
#refer to https://stackoverflow.com/questions/23897809/different-results-in-go-and-pycrypto-when-using-aes-cfb
def decrypt(key, ct, iv):
	padlen = 16 - (len(ct) % 16)
	aes = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
	return aes.decrypt(ct + "#"*padlen)[:len(ct)]

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

#refer to PGP packet(https://tools.ietf.org/html/rfc4880#section-5.3)
def processEskPacket(m, passphrase):
	salt = m[6:14]
	#print "salt : " + hex(bytes_to_long(salt))
	cnt = ord(m[14])
	cnt = (16 + (cnt & 15)) << ((cnt >> 4) + 6)
	#print cnt

	#should check m[3] to get the key size
	#in this case, m[3] was 09(AES256), so keylen is 32
	return getKey(passphrase, salt, cnt, 32)

#refer to PGP encryption(https://www.ssi.gouv.fr/uploads/2015/05/format-Oracles-on-OpenPGP.pdf)
def processEncMDCPacket(m, sessionkey):
	ct = m[3:]

	pt = decrypt(sessionkey, ct, '\x00' * 16)
	#print "pt : " + hex(bytes_to_long(pt))

	#index is depends on the size of cipher block size. AES => 16
	if not(pt[14] == pt[16] and pt[15] == pt[17]):
		print "Wrong session key!!"
		return ""

	#remove MDC part(2 byte + SHA1 hash)
	pt = pt[18:-22]
	#print "pt : " + hex(bytes_to_long(pt))
	#print len(pt)
	#print pt

	return pt

def processCompressedPacket(m):
	compressed = m[2:]

	#addtional argument for deflate date according to RFC1951
	#refer to https://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations
	m = zlib.decompress(compressed, -zlib.MAX_WBITS)
	#print "text : " + hex(bytes_to_long(m))

	#remove literal packet header(classifier, date)
	return m[8:]


#'''
url = "http://drinks.teaser.insomnihack.ch/generateEncryptedVoucher"

data = {"recipientName" : "matta", "drink" : "beer"}
headers = {"Content-type" : "application/json"}

resp = requests.post(url, json=data, headers=headers)
m = resp.text
print m
'''
m = """-----BEGIN DRINK VOUCHER-----

jA0ECQMCBP4JEzSWQd//0l0BOpx5GsIKV/uioGot3PhzSku072+payEaIK3mgEuZ
hWuwOvYtxB/TRCoJdq+SmrpN9qAPtUcyMyvA736R6jMHIb2iEm2ZqpntQnqyJ5Vj
6BeksTMQH+DpsGn8YTw=
=GP0x
-----END DRINK VOUCHER-----

m"""
#'''

packets = getPackets(m)

sessionKey = processEskPacket(packets, "G1MME_B33R_PLZ_1M_S0_V3RY_TH1RSTY")
m = processEncMDCPacket(packets[15:], sessionKey)
print processCompressedPacket(m)

