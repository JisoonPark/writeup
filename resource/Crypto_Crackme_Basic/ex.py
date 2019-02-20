from Crypto.Cipher import DES
import base64

obj = DES.new('BluSH4G*', DES.MODE_ECB)

cipher = base64.b64decode('7A38V6xRUofPwAj1THUFmbqNgf9CeCR7Jcp1c4F1pe/g2Bzodq7delcwt7bsML8R')

plain = obj.decrypt(cipher)
print plain
