import os
import sys
import struct
import gmpy2
from socket import *
from Crypto.Hash import SHA256, MD5
from Crypto.Util import number

ADDR = ("10.113.108.125", 30303)

def readline(sock):
    r = ""
    while True:
        c = sock.recv(1)
        if c == '\n':
            return r
        r += c

def sendline(sock, m):
    sock.send(m)
    sock.send('\n')
    return

def POW(sock):
    #get challenge
    sm = readline(sock)
    challenge = sm[-12:].decode('hex')

    #find suitable message
    i = 0
    while (MD5.new(challenge + str(i)).hexdigest().endswith('fffff') == False):
	    i += 1

    sendline(sock, (challenge + str(i)).encode('hex'))
    return

def hid(name):
    return number.bytes_to_long(SHA256.new(name).digest())

def connect(addr):
    sock = socket(AF_INET, SOCK_STREAM)

    try:
	    sock.connect(ADDR)
    except Exception as e:
	    print ("Connection failed (%s:%s)" % ADDR)
	    sys.exit()
    return sock

def skip_menu(sock):
    POW(sock)           #proof of work
    readline(sock)      #welcome message
    readline(sock)      #menu message
    readline(sock)      #menu message
    readline(sock)      #menu message
    return

def get_sk(name):
    #connect
    sock = connect(ADDR)

    skip_menu(sock)

    sendline(sock, "1") #select register
    readline(sock)      #"id?"
    sendline(sock, name)

    #read pk
    sm = readline(sock)
    pk = int(sm[len("Server public key : "):], 16)

    #read client's sk
    sm = readline(sock)
    csk = int(sm[len("Your secret key : "):], 16)
    
    sock.close()

    return pk, csk   

def get_flag(name, hid, pk, ssk):
    #connect
    sock = connect(ADDR)
    
    skip_menu(sock)
    
    sendline(sock, "2")     #select read
    readline(sock)          #"What is your id?"
    sendline(sock, name)
    sm = readline(sock)     #"Pls sign on it"
    rnd = int(sm[len("Pls sign on it : "):], 16)
    sign = pow(ssk, hid * rnd, pk)
    sendline(sock, hex(sign))

    readline(sock)    #'Welcome'
    flag = readline(sock)    #flag message
    
    sock.close()

    return flag

if __name__ == '__main__':
    print "pwning started"
    id1, id2, id3 = 'iam', 'jisoon', 'admin'

    hid1, hid2, hid3 = hid(id1), hid(id2), hid(id3)

    g, a, b = gmpy2.gcdext(hid1, hid2)
    assert g == 1 and a * hid1 + b * hid2 == 1

    pk, csk1 = get_sk(id1)
    print "phase 1 end"

    pk, csk2 = get_sk(id2)
    print "phase 2 end"

    #find server's sk
    ssk = pow(csk1, a, pk) * pow(csk2, b, pk) % pk
    assert pow(ssk, hid1, pk) == csk1 and pow(ssk, hid2, pk) == csk2

    flag = get_flag(id3, hid3, pk, ssk)
    print "phase 3 end"
    
    print "flag : " + flag

