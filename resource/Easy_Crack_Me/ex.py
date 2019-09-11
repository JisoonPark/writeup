import itertools
import subprocess
candidate = map(ord, "012456789abcdef")

sums = [0x15e, 0xda, 0x12f, 0x131, 0x100, 0x131, 0xfb, 0x102]
xors = [0x52, 0xc, 1, 0xf, 0x5c, 5, 0x53, 0x58]

sums_xors = [(s, x) for s, x in zip(sums, xors)]
sum_xor_candidates = [set(), set(), set(), set(), set(), set(), set(), set()]

form = "-f_-_87_-__--__-_2-_--___4-___-5"
def check(idx, n):
	for i in range(4):
		c = form[idx * 4 + i]
		if c == '-':
			if not n[i] in candidate[9:]:
				return False
		elif c == "_":
			if not n[i] in candidate[:9]:
				return False
		else:
			if n[i] != ord(c):
				return False
	return True

for p in itertools.product(candidate, repeat=4):
	summ = reduce(lambda x, y:x+y, p)
	lxor = reduce(lambda x, y:x^y, p)

	for idx, (check_s, check_x) in enumerate(sums_xors):
		if summ == check_s and lxor == check_x:
			if check(idx, p):
				(sum_xor_candidates[idx]).add(p)

#print [len(x) for x in sum_xor_candidates]
#[5, 4, 82, 48, 6, 64, 18, 8]

sums = [0x129, 0x103, 0x12b, 0x131, 0x135, 0x10b, 0xff, 0xff]
xors = [1, 0x57, 7, 0xd, 0xd, 0x53, 0x51, 0x51]

sums_xors = [(s, x) for s, x in zip(sums, xors)]

for li in range(2):
	for lj in range(4):
		sum_xor_candidates2 = [set(), set(), set(), set(), set(), set(), set(), set()]

		for s1 in sum_xor_candidates[li]:
			for s2 in sum_xor_candidates[li + 2]:
				for s3 in sum_xor_candidates[li + 4]:
					for s4 in sum_xor_candidates[li + 6]:
						summ = s1[lj] + s2[lj] + s3[lj] + s4[lj]
						lxor = s1[lj] ^ s2[lj] ^ s3[lj] ^ s4[lj]

						if (summ, lxor) == sums_xors[li * 4 + lj]:
							(sum_xor_candidates2[li]).add(s1)
							(sum_xor_candidates2[li + 2]).add(s2)
							(sum_xor_candidates2[li + 4]).add(s3)
							(sum_xor_candidates2[li + 6]).add(s4)

		sum_xor_candidates[li] = sum_xor_candidates2[li]
		sum_xor_candidates[li + 2] = sum_xor_candidates2[li + 2]
		sum_xor_candidates[li + 2] = sum_xor_candidates2[li + 2]
		sum_xor_candidates[li + 2] = sum_xor_candidates2[li + 2]

#print [len(x) for x in sum_xor_candidates]
i = 0
cnt = [0] * 16
for s0 in sum_xor_candidates[0]:
	cnt[int(chr(s0[0]), 16)] += 1
	cnt[int(chr(s0[1]), 16)] += 1
	cnt[int(chr(s0[2]), 16)] += 1
	cnt[int(chr(s0[3]), 16)] += 1
	for s1 in sum_xor_candidates[1]:
		cnt[int(chr(s1[0]), 16)] += 1
		cnt[int(chr(s1[1]), 16)] += 1
		cnt[int(chr(s1[2]), 16)] += 1
		cnt[int(chr(s1[3]), 16)] += 1
		for s2 in sum_xor_candidates[2]:
			cnt[int(chr(s2[0]), 16)] += 1
			cnt[int(chr(s2[1]), 16)] += 1
			cnt[int(chr(s2[2]), 16)] += 1
			cnt[int(chr(s2[3]), 16)] += 1
			for s3 in sum_xor_candidates[3]:
				#print i
				#i += 1
				cnt[int(chr(s3[0]), 16)] += 1
				cnt[int(chr(s3[1]), 16)] += 1
				cnt[int(chr(s3[2]), 16)] += 1
				cnt[int(chr(s3[3]), 16)] += 1
				for s4 in sum_xor_candidates[4]:
					cnt[int(chr(s4[0]), 16)] += 1
					cnt[int(chr(s4[1]), 16)] += 1
					cnt[int(chr(s4[2]), 16)] += 1
					cnt[int(chr(s4[3]), 16)] += 1
					for s5 in sum_xor_candidates[5]:
						cnt[int(chr(s5[0]), 16)] += 1
						cnt[int(chr(s5[1]), 16)] += 1
						cnt[int(chr(s5[2]), 16)] += 1
						cnt[int(chr(s5[3]), 16)] += 1
						for s6 in sum_xor_candidates[6]:
							cnt[int(chr(s6[0]), 16)] += 1
							cnt[int(chr(s6[1]), 16)] += 1
							cnt[int(chr(s6[2]), 16)] += 1
							cnt[int(chr(s6[3]), 16)] += 1
							for s7 in sum_xor_candidates[7]:
								cnt[int(chr(s7[0]), 16)] += 1
								cnt[int(chr(s7[1]), 16)] += 1
								cnt[int(chr(s7[2]), 16)] += 1
								cnt[int(chr(s7[3]), 16)] += 1

								#print cnt
								if cnt == [3, 2, 2, 0, 3, 2, 1, 3, 3, 1, 1, 3, 1, 2, 2, 3]:
									#print s0, s1, s2, s3, s4, s5, s6, s7
									l = list(s0) + list(s1) + list(s2) + list(s3) + list(s4) + list(s5) + list(s6) + list(s7)
									if reduce(lambda x, y: x + y, l[::2]) == 1160:
										ss = subprocess.check_output(["./easy_crack_me", "TWCTF{" + "".join(map(chr, l)) + "}"]).strip()
										if ss.startswith("Correct:"):
											print ss
											exit()

								cnt[int(chr(s7[0]), 16)] -= 1
								cnt[int(chr(s7[1]), 16)] -= 1
								cnt[int(chr(s7[2]), 16)] -= 1
								cnt[int(chr(s7[3]), 16)] -= 1

							cnt[int(chr(s6[0]), 16)] -= 1
							cnt[int(chr(s6[1]), 16)] -= 1
							cnt[int(chr(s6[2]), 16)] -= 1
							cnt[int(chr(s6[3]), 16)] -= 1

						cnt[int(chr(s5[0]), 16)] -= 1
						cnt[int(chr(s5[1]), 16)] -= 1
						cnt[int(chr(s5[2]), 16)] -= 1
						cnt[int(chr(s5[3]), 16)] -= 1

					cnt[int(chr(s4[0]), 16)] -= 1
					cnt[int(chr(s4[1]), 16)] -= 1
					cnt[int(chr(s4[2]), 16)] -= 1
					cnt[int(chr(s4[3]), 16)] -= 1

				cnt[int(chr(s3[0]), 16)] -= 1
				cnt[int(chr(s3[1]), 16)] -= 1
				cnt[int(chr(s3[2]), 16)] -= 1
				cnt[int(chr(s3[3]), 16)] -= 1

			cnt[int(chr(s2[0]), 16)] -= 1
			cnt[int(chr(s2[1]), 16)] -= 1
			cnt[int(chr(s2[2]), 16)] -= 1
			cnt[int(chr(s2[3]), 16)] -= 1

		cnt[int(chr(s1[0]), 16)] -= 1
		cnt[int(chr(s1[1]), 16)] -= 1
		cnt[int(chr(s1[2]), 16)] -= 1
		cnt[int(chr(s1[3]), 16)] -= 1

	cnt[int(chr(s0[0]), 16)] -= 1
	cnt[int(chr(s0[1]), 16)] -= 1
	cnt[int(chr(s0[2]), 16)] -= 1
	cnt[int(chr(s0[3]), 16)] -= 1
