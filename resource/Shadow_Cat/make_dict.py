import itertools

a = "abcdefghijklmnopqrstuvwxyz"

f = open("dict.txt", "w")

for c in a:
	f.write(c + "\n")

for c in itertools.product(a, repeat=2):
	f.write("".join(c) + "\n")

for c in itertools.product(a, repeat=3):
	f.write("".join(c) + "\n")
