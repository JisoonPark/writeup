from Crypto.PublicKey import RSA
from Crypto.Util.number import *

#e, n, c
params = open("parameters.txt").read().split("\n")

for l in params:
	if len(l) == 0:
		continue
	exec(l)

'''
#export public key pair to public.pem
public_key = RSA.construct((n, e))

with open("public.pem", "w") as f:
	f.write(public_key.exportKey(format='PEM'))
'''

'''
generate private.pem by using RsaCtfTool
'''

privdata = open("private.pem").read()
private_key = RSA.importKey(privdata)

print private_key.decrypt(long_to_bytes(c))
