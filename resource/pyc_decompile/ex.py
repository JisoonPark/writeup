import time
from sys import exit
from hashlib import sha512
import requests

def make_flag():
    now = time.localtime(time.time())
    seed = time.strftime('%m/%d/HJEJSH', time.localtime())
    hs = sha512(seed).hexdigest()
    start = now.tm_hour % 3 + 1
    end = start * ((now.tm_min + 2) % 30 + 10)
    ok = hs[start:end]
    return ok

URL = 'http://wargame.kr:8080/pyc_decompile'
data = {'flag' : make_flag()}

response = requests.get(URL, params = data)

#print "server time : " + response.headers['Date']
#print "local time  : " + time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

print response.text
