import json

data = ""
r = dict()

def parse_http(js):
	global r
	for d in js:
		iterate(d, 0, "urlencoded-form.value")
		m = data.decode("hex").split(".")
		#print m
		r[int(m[1])] = m[2]

def parse_icmp(js):
	global r
	for d in js:
		iterate(d, 0, "data.data")
		if len(data) < 600: continue
		m = data.replace(":", "").decode("hex").decode("hex").split(".")
		#print m
		r[int(m[1])] = m[2]

def parse_dns(js):
	global r
	a = ""
	for d in js:
		iterate(d, 0, "dns.qry.name")
		t = data.split(".")[1]
		if (len(a) > 0 and t.startswith("53457834495256")):
			m = a.decode("hex").split(".")
			#print m
			r[int(m[1])] = m[2]
			a = ""
		a += t

def iterate(d, depth, k):
	for (key, val) in d.iteritems():
		if key == k: 
			global data
			data = str(val)
			break
		if type(val) is dict:
			iterate(val, depth + 1, k)

json_file = open("export1.json", "r").read()
js = json.loads(json_file)

parse_http(js)

json_file = open("export2.json", "r").read()
js = json.loads(json_file)

parse_icmp(js)

json_file = open("export3.json", "r").read()
js = json.loads(json_file)

parse_dns(js)

with open("output", "w") as f:
	for i in range(51):
		f.write(r[i].decode("hex"))
