import requests
import sys

site = sys.argv[1]
url = f'https://{site}/?search=<script>'
resp = requests.get(url)

print(f"[*] Status code: {resp.status_code}")
print(f"[*] Response preview:\n{resp.text[:300]}...\n")