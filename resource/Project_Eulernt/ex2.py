import gmpy2
import itertools
import time

start = time.time()

N = int(gmpy2.fac(333))
sN = int(gmpy2.isqrt(N))

p_d = [ 
(2,328), (3,165), (5,81), (7,53), (11,32), (13,26), (17,20), (19,17), (23,14), (29,11), (31,10), (37,9), (41,8), (43,7), (47,7), (53,6), (59,5), (61,5), (67,4), (71,4), (73,4), (79,4), (83,4), 
 (89,3), (97,3), (101,3), (103,3), (107,3), (109,3), (113,2), (127,2), (131,2), (137,2), (139,2),
  (149,2), (151,2), (157,2), (163,2), (167,1), (173,1), (179,1), (181,1), (191,1), (193,1),
   (197,1), (199,1), (211,1), (223,1), (227,1), (229,1), (233,1), (239,1), (241,1), (251,1), (257,1), (263,1), (269,1), (271,1), (277,1), (281,1), (283,1), (293,1), (307,1), (311,1), (313,1), (317,1), (331,1) 
]

prefix = 1
nums = []
for (a, b) in p_d:
	if b & 1 == 1:
		nums.append(a)
	prefix *= (a ** (b / 2))

print "prefix(x)", prefix
print "remained(y)", nums

a = 1
b = 1

l1 = []
l2 = []

#1. init
for i in range(2, len(nums) - 1, 2):
	c = abs(a * nums[i] - b * nums[i + 1])
	d = abs(a * nums[i + 1] - b * nums[i])

	if (c < d):
		#c is better
		a *= nums[i]
		b *= nums[i + 1]
		l1.append(nums[i])
		l2.append(nums[i + 1])
	else:
		a *= nums[i + 1]
		b *= nums[i]
		l1.append(nums[i + 1])
		l2.append(nums[i])

#if there's one remained
if len(nums) & 1 == 1:
	if a < b:
		a *= nums[-1]
		l1.append(nums[-1])
	else:
		b *= nums[-1]
		l2.append(nums[-1])

'''
print sN // prefix
print a
print b
print l1
print l2
'''

#2. make candidates
depth = 5
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
target = (sN // prefix) * 1.0 / a
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
			if abs(int((diff + target) * a) * prefix - sN) * 10**8 < sN:
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

a = reduce(lambda a, b: a * b, l1) * prefix
b = reduce(lambda a, b: a * b, l2) * prefix

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

print "elapsed time", time.time() - start
