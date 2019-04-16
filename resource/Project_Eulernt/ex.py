import gmpy2
import itertools

N = int(gmpy2.fac(333))
sN = int(gmpy2.isqrt(N))

a = 1
b = 1

l1 = []
l2 = []

#1. init
for i in range(2, 333, 2):
	c = abs(a * i - b * (i + 1))
	d = abs(a * (i + 1) - b * i)

	if (c < d):
		#c is better
		a *= i
		b *= i + 1
		l1.append(i)
		l2.append(i + 1)
	else:
		a *= i + 1
		b *= i
		l1.append(i + 1)
		l2.append(i)

#2. make candidates
depth = 3
s1 = [(i, (i,)) for i in l1]
s2 = [(i, (i,)) for i in l2]

for depth in range(2, depth + 1):
	for l in itertools.combinations(l1, depth):
		e = (reduce(lambda x, y:x*y, l), l)
		s1.append(e)
	for l in itertools.combinations(l2, depth):
		e = (reduce(lambda x, y:x*y, l), l)
		s2.append(e)

#3 find best, shift for float max range
target = (sN >> 1024) * 1.0 / (a >> 1024)
print target
m = (s2[0][0] * 1.0 / s1[0][0], 0, 0)
for (i1, ls1) in s1:
	for (i2, ls2) in s2:
		if i1 == i2:
			continue
		diff = abs((i2 * 1.0 / i1) - target)
		if diff < m[0]:
			m = (diff, ls1, ls2)
			print m
			if diff < 0.00000001:
				m = (0, ls1, ls2)
				break
	if m[0] == 0:
		break

for i in m[1]:
	l1.remove(i)
	l2.append(i)
for i in m[2]:
	l1.append(i)
	l2.remove(i)

a = reduce(lambda a, b: a * b, l1)
b = reduce(lambda a, b: a * b, l2)

print l1
print l2
print a
print b
print (sN >> 1024) * 1.0 / (a >> 1024)
print (sN >> 1024) * 1.0 / (b >> 1024)

if abs(a - sN) * 10**8 < sN:
	print "=" * 100
	print "got it!:"
	print a
	print "=" * 100
if abs(b - sN) * 10**8 < sN:
	print "=" * 100
	print "got it!:"
	print b
	print "=" * 100
