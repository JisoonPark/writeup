jtl_res = """w                (l)
h                (v)
f                (w)
a                (a)
l                (r)
m                (g)
k                (b)
t                (u)
c                (q)
s                (j)
r                (y)
x                (o)
u                (k)
y                (p)
b                (x)
d                (s)
z                (_)
v                (i)
j                (f)
g                (d)
q                (m)
p                (h)
n                (n)
e                (c)
i                (e)
o                (t)
_                (_)"""

target = "hajjzvajvzqyaqbendzvajvqauzarlapjzrkybjzenzuvczjvastlj"

d = dict()
for l in jtl_res.split("\n"):
	key, data = l.split("                ")
	d[key] = data[1]


for i in range(500):
	r = ""
	for c in target:
		r += d[c]
	target = r
	if r.startswith("pass_") and r.endswith("_shadows"):
		print (i, "VolgaCTF{" + r + "}")
