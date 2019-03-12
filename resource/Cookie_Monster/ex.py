import requests

URL = 'http://159.89.166.12:13500/'

cookies = dict()
initial_v = ""
while True:
	response = requests.get(URL, cookies=cookies)
	#print response.headers

	if "Set-Cookie" in response.headers:
		k, v = response.headers["Set-Cookie"].split('=')
		cookies[k] = v
		if initial_v == v:
			break
		if len(initial_v) == 0:
			initial_v = v
		print v
