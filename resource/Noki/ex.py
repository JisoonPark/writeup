import string

ct = "g4iu{ocs_oaeiiamqqi_qk_moam!}e0gi"

d = dict()
for i in range(26):
	k = string.lowercase[i * 2 % 26]
	if k in d:
		d[k] = d[k] + string.lowercase[i]
	else:
		d[k] = string.lowercase[i]

words = open("/home/matta/tools/dictionary/words_alpha.txt").readlines()
words = [w.strip() for w in words]

def get_words(s):
	w = filter(lambda x: len(x) == len(s), words)
	for i, c in enumerate(s):
		w = filter(lambda x: x[i] in d[c], w)

	return w

ct = ct[ct.index("{") + 1:ct.index("!}")].split("_")

print "d4rk{" + "_".join(["|".join(get_words(s)) for s in ct]) + "!}c0de"
