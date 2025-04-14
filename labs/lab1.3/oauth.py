import requests
from bs4 import BeautifulSoup
import re

site = '0ad700fc038ea101804f17fe00ea0062.web-security-academy.net'  # your site
s = requests.Session()

# Step 1 - Start OAuth flow
login_url = f'https://{site}/social-login'
resp = s.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
meta = soup.find('meta', {'http-equiv': 'refresh'})
auth_url = meta['content'].split(';')[1].lstrip('url=')
oauth_site = auth_url.split('/')[2]

# Step 2 - Log in to identity provider
resp = s.get(auth_url)
soup = BeautifulSoup(resp.text, 'html.parser')
login = soup.find('form')
login_url = f"https://{oauth_site}{login['action']}"
resp = s.post(login_url, data={'username': 'wiener', 'password': 'peter'})

# Step 3 - Consent form
soup = BeautifulSoup(resp.text, 'html.parser')
cont = soup.find('form')
cont_url = f"https://{oauth_site}{cont['action']}"

# Step 4 - Follow manual redirects
resp = s.post(cont_url, allow_redirects=False)
redir_url_1 = resp.headers["Location"]
resp = s.get(redir_url_1, allow_redirects=False)
redir_url_2 = resp.headers["Location"]

# Step 5 - Extract token
token = re.split('[#&]', redir_url_2)[1].split('=')[1]
print(f'[+] Access token is: {token}')
