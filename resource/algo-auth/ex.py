from pwn import *
import copy

def min_path_sum2(matrix):
	res = copy.deepcopy(matrix)
	for i in range(7):
		for j in range(7):
			res[i][j] = matrix[j][6 - i]

	for i in range(1, 7):
		for j in range(7):
			res[i][j] = res[i - 1][j] + matrix[j][6 - i]

		while True:
			update = 0
			t = res[i][0]
			res[i][0] = min(res[i][0], res[i][1] + matrix[0][6 - i])
			if (res[i][0] < t):  update = 1

			t = res[i][6]
			res[i][6] = min(res[i][6], res[i][5] + matrix[6][6 - i])
			if (res[i][6] < t):  update = 1

			for j in range(1, 6):
				t = res[i][j]
				res[i][j] = min(res[i][j], matrix[j][6 - i] + res[i][j - 1], matrix[j][6 - i] + res[i][j + 1])
				if (res[i][j] < t):  update = 1

			if not update: break

	return min(res[6])

r = remote('110.10.147.104', 15712)

r.recvuntil(">> ")
r.sendline("G")

s = ""
for i in range(100):
	if i == 0: r.readline()
	m = r.recvuntil(">>> ")
	print m
	matrix = [[int(n) for n in line.strip().split()] for line in m.split('\n')[1:-2]]
	#print matrix
	sol = min_path_sum2(matrix)

	s += chr(sol)
	print s

	r.sendline(str(sol))

r.interactive()