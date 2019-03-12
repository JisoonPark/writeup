def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
if __name__ == '__main__':
    n, a = [], []
    v12 = 213;
    v13 = 8;
    v14 = 229;
    v15 = 5;
    v16 = 25;
    v17 = 4;
    v18 = 83;
    v19 = 7;
    v20 = 135;
    v21 = 5;
    v3 = int("27644437104591489104652716127"[0:v13])
    n.append(v3)
    a.append(v12)
    v9 = v13;
    v4 = int("27644437104591489104652716127"[v13:v13 + v15])
    n.append(v4)
    a.append(v14)
    v10 = v15 + v9;
    v5 = int("27644437104591489104652716127"[v10:v10 + v17])
    n.append(v5)
    a.append(v16)
    v11 = v17 + v10;
    v6 = int("27644437104591489104652716127"[v11:v11 + v19])
    n.append(v6)
    a.append(v18)
    v8 = int("27644437104591489104652716127"[v19 + v11:v19 + v11 + v21])
    n.append(v8)
    a.append(v20)

    key = chinese_remainder(n, a)

    v12 = str(key) + "27644437104591489104652716127" + "80"

    matrix = open("matrix.txt").read()
    passwd = ""

    v7 = 0;
    v8 = 0;
    v10 = len(v12) >> 1;
    while ( v8 < (len(v12) >> 1) ):
        passwd += matrix[100 * (10 * (ord(v12[v8]) - 48) + ord(v12[v8 + 1]) - 48) - 48 + 10 * (ord(v12[v10]) - 48) + ord(v12[v10 + 1])]
        ++v7;
        v8 += 2;
        v10 += 2;
    v9 = 0;
    v11 = len(v12) >> 1;
    while ( v9 < (len(v12) >> 1 )):
        v4 = 10 * (ord(v12[v9]) - 48) + ord(v12[v9 + 1]) - 48;
        v5 = 10 * (ord(v12[v11]) - 48) + ord(v12[v11 + 1]) - 48;
        passwd += matrix[100 * (v4 * v4 % 97) + v5 * v5 % 97]
        ++v7;
        v9 += 2;
        v11 += 2;

    print passwd
