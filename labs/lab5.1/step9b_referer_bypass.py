import requests

site = '0ac7002603526cb885e9d53000b8005d.web-security-academy.net'
login_url = f'https://{site}/login'
referer_url = f'https://{site}/login'

logindata = {
    'username': 'wiener',
    'password': 'peter'
}

headers = {
    'Referer': referer_url
}

resp = requests.post(login_url, data=logindata, headers=headers)
print(f"HTTP status code: {resp.status_code}")
print(f"Response text: {resp.text[:300]}")