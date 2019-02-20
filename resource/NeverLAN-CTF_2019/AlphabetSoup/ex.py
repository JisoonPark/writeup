import itertools

text = "MKXU IDKMI DM BDASKMI NLU XCPJNDICFQ! K VDMGUC KW PDT GKG NLKB HP LFMG DC TBUG PDTC CUBDTCXUB. K'Q BTCU MDV PDT VFMN F WAFI BD LUCU KN KB WAFI GDKMINLKBHPLFMGKBQDCUWTMNLFMFMDMAKMUNDDA"
prob = text.replace("!", "").replace(".", "").split()[:-1]

'''
words = open("words.txt", "r").read()
word_list = words.split()

lst = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for word in word_list:
	if len(word) == 4 and word[0] == 'f' and word[2] == "a":
		print word
'''
d = dict()
d['K'] = 'i'
d['Q'] = 'm'

#iN iB => it is
d['N'] = 't'
d['B'] = 's'

#tLis => this
d['L'] = 'h'

#F => a
d['F'] = 'a'

#hUCU => here
d['U'] = 'e'
d['C'] = 'r'

#sD => so
d['D'] = 'o'

#sTre => sure
d['T'] = 'u'

#i VoMGer iW Pou GiG => i wonder if you did
d['V'] = 'w'
d['M'] = 'n'
d['G'] = 'd'
d['W'] = 'f'
d['P'] = 'y'

#niXe => nice
d['X'] = 'c'

#Hy hand => by hand
d['H'] = 'b'

#doinI => doing
d['I'] = 'g'

# soASing => solving
d['A'] = 'l'
d['S'] = 'v'

#cryJtogram => cryptogram
d['J'] = 'p'

r = ""
for c in text:
	if c in d:
		r += d[c]
	else:
		r += c

print r

