import json

data = open("users_db", "r").read().replace("\n", "")
data = data.decode("hex").strip()
data = data.decode("base64")

def iterate(d, depth):
	for (key, val) in d.iteritems():
		if "flag" in key: 
			print key
			print val
		if type(val) is unicode:
			#print "  " * depth + key + " : " + val
			if "flag" in val: print val
		else:
			#print "  " * depth + key + " : "
			iterate(val, depth + 1)

y = json.loads("{" + data[2:])

iterate(y, 0)

