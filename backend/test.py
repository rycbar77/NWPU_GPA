import requests
data = {
    'username': '',
    'password': ''
}
s = requests.post('http://127.0.0.1:5590/', data=data)
s.encoding = 'utf-8'
print(s.text)
