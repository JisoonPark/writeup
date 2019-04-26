# modified source code from force32.py (https://www.nayuki.io/page/forcing-a-files-crc-to-any-value)
# the original code is maintained under GPL 3.0 license, and following is the comment from original source code.
# 
# CRC-32 forcer (Python)
# Compatible with Python 2 and 3.
# 
# Copyright (c) 2017 Project Nayuki
# https://www.nayuki.io/page/forcing-a-files-crc-to-any-value
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program (see COPYING.txt).
# If not, see <http://www.gnu.org/licenses/>.
# 


from zlib import crc32
import string, random

# ---- Utilities ----

POLYNOMIAL = 0x104C11DB7  # Generator polynomial. Do not modify, because there are many dependencies
MASK = (1 << 32) - 1

def get_crc32(data):
	crc = crc32(data, 0)
	return reverse32(crc & MASK)

def reverse32(x):
	y = 0
	for i in range(32):
		y = (y << 1) | (x & 1)
		x >>= 1
	return y

# ---- Polynomial arithmetic ----

# Returns polynomial x multiplied by polynomial y modulo the generator polynomial.
def multiply_mod(x, y):
	# Russian peasant multiplication algorithm
	z = 0
	while y != 0:
		z ^= x * (y & 1)
		y >>= 1
		x <<= 1
		if (x >> 32) & 1 != 0:
			x ^= POLYNOMIAL
	return z


# Returns polynomial x to the power of natural number y modulo the generator polynomial.
def pow_mod(x, y):
	# Exponentiation by squaring
	z = 1
	while y != 0:
		if y & 1 != 0:
			z = multiply_mod(z, x)
		x = multiply_mod(x, x)
		y >>= 1
	return z


# Computes polynomial x divided by polynomial y, returning the quotient and remainder.
def divide_and_remainder(x, y):
	if y == 0:
		raise ValueError("Division by zero")
	if x == 0:
		return (0, 0)
	
	ydeg = get_degree(y)
	z = 0
	for i in range(get_degree(x) - ydeg, -1, -1):
		if (x >> (i + ydeg)) & 1 != 0:
			x ^= y << i
			z |= 1 << i
	return (z, x)



# Returns the reciprocal of polynomial x with respect to the modulus polynomial m.
def reciprocal_mod(x):
	# Based on a simplification of the extended Euclidean algorithm
	y = x
	x = POLYNOMIAL
	a = 0
	b = 1
	while y != 0:
		q, r = divide_and_remainder(x, y)
		c = a ^ multiply_mod(q, b)
		x = y
		y = r
		a = b
		b = c
	if x == 1:
		return a
	else:
		raise ValueError("Reciprocal does not exist")


def get_degree(x):
	return x.bit_length() - 1

def modify_crc32(data, offset, newcrc, printstatus=False):
	length = len(data)
	if offset + 4 > length:
		raise ValueError("Byte offset plus 4 exceeds file length")
	
	# Read entire file and calculate original CRC-32 value
	crc = get_crc32(data)
	if printstatus:
		print("Original CRC-32: {:08X}".format(reverse32(crc)))

	# Compute the change to make
	delta = crc ^ newcrc
	delta = multiply_mod(reciprocal_mod(pow_mod(2, (length - offset) * 8)), delta)
	
	# Patch 4 bytes in the file
	bytes4 = bytearray(data[offset:offset + 4])
	if len(bytes4) != 4:
		raise IOError("Cannot read 4 bytes at offset")
	for i in range(4):
		bytes4[i] ^= (reverse32(delta) >> (i * 8)) & 0xFF

	data = data[:offset] + str(bytes4) + data[offset + 4:]
	if printstatus:
		print("Computed and wrote patch")
	
	# Recheck entire file
	if get_crc32(data) != newcrc:
		return None
	elif printstatus:
		print("New CRC-32 successfully verified")

	return data

s = string.letters + string.digits

def is_printable(msg):
	for c in msg:
		if ord(c) < 32 or ord(c) > 126 or c in "\n\t\r^\",":
			return False
	return True

def get_crc_pair(l):
	l -= 6
	while True:
		r1 = "ASIS{" + "".join([random.choice(s) for _ in range(l)]) + "}"
		crc = get_crc32(r1)
		if crc < 0:
			continue

		r2 = "ASIS{" + "".join([random.choice(s) for _ in range(l)]) + "}"

		for i in range(5, l + 2):
			r2 = modify_crc32(r2, i, crc, False)

			if r1 != None and crc32(r1) == crc32(r2) and is_printable(r2):
				print "\"%d\":\"%s,%s\""%(l + 6, r1, r2)
				return "%s,%s"%(r1, r2)
