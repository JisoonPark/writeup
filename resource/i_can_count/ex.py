
def rol(a1, a2):
    v1 = a1 << a2
    if (a2 & 0x20):
        v1 = (v1 & 0xffffffff) << 32

    v2 = a1 >> ((48 - a2) & 0x1f)
    if (48 - a2) & 0x20:
        v2 >>= 32

    r = (v1 | v2) & 0xffffffffffff
    #print hex(r)
    return r

flagbuf = map(ord, list("\x93\x42\x05\x93\x04\xCD\x7F\x78\x42\x78\x05\xCD\xCD\x42\x42\x78\xCD\xB5\xB5\x89\x00"))

i = -1
flag = ""
while True:
    i += 1
    if (i > 19):
        print "PCTF{%s}"%flag
        break
    for c in "1234567890":
        v0 = ord(c)
        v1 = v0 & 3
        v2 = (v0 >> 2) & 3
        v3 = (v0 >> 4) & 0xF

        v4 = rol(v1 + 0xA55AA55AA559, 2)
        v5 = v4
        v6 = rol(v2 - v4 + 0xA55AA55AA559, 13)
        v7 = v6
        v8 = rol(v3 - v6 + 0xA55AA55AA559, 17)
        v9 = v8
        v10 = v7 ^ v8 ^ v5
        v11 = rol((v7 & ~(v7 ^ v8 ^ v5) | v8 & (v7 ^ v8 ^ v5)) + v5 + v3 + 68453106630, 3)
        v12 = v11
        v13 = rol((v9 & ~v11 | v10 & v11) + v7 + v1 + 68453106630, 11)
        v14 = v13
        v15 = rol((v12 & ~v9 | v13 & v9) + v10 + v2 + 68453106630, 19)
        v16 = v15
        v17 = rol((v14 ^ v9 ^ v15) + v12 + v2 + 201504941903014, 5)
        v18 = v17
        v19 = rol((v16 ^ v17 ^ v14) + v9 + v1 + 201504941903014, 7)
        v20 = v19
        v21 = rol((v18 ^ v14 ^ v19) + v16 + v3 + 201504941903014, 23)
        #print hex(v20 + v21 + v18 + v14)
        v22 = (((v20 + v21 + v18 + v14) >> 32) & 0xFFFFFFFF) ^ (v20 + v21 + v18 + v14)
        v23 = (v22 >> 16) ^ v22
        r = (v23 & 0xff) ^ ((v23 >> 8) & 0xff)
        #print (hex(flagbuf[i]), hex(r))
        if flagbuf[i] == r:
            flag += c
            print i, c, flag
            break
