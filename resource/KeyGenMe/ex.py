'''
_BYTE *__fastcall enc(const char *a1)
{
  unsigned __int8 v2; // [rsp+1Fh] [rbp-11h]
  int i; // [rsp+20h] [rbp-10h]
  int v4; // [rsp+24h] [rbp-Ch]
  _BYTE *v5; // [rsp+28h] [rbp-8h]

  v5 = malloc(0x40uLL);
  v4 = strlen(a1);
  v2 = 72;
  for ( i = 0; i < v4; ++i )
  {
    v5[i] = ((a1[i] + 12) * v2 + 17) % 70 + 48;
    v2 = v5[i];
  }
  return v5;
}
'''



def enc(a1):
	v4 = len(a1)
	v2 = 72
	r = ""
	for i in range(v4):
		v2 = ((ord(a1[i]) + 12) * v2 + 17) % 70 + 48;
		r += chr(v2)
	return r

def dec(a1):
	v4 = len(a1)
	v2 = 72
	r = ""
	for i in range(v4):
		for j in range(ord('A'), ord('z') + 1):
			t = ((j + 12) * v2 + 17) % 70 + 48
			if t == ord(a1[i]):
				r += chr(j)
				break
		v2 = ord(a1[i])
	return r

target = "[OIonU2_<__nK<KsK"
d = dec(target[:-1])
print "dec : " + d
e = enc(d + "\n")
print "enc : " + e

if e == target:
	print "OK!"
else:
	print "Fail!"

