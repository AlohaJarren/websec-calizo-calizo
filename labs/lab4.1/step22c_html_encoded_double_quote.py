import requests
from bs4 import BeautifulSoup

site = '0a2c00ba03df227a806b121a00410012.web-security-academy.net'
s = requests.Session()

def try_post(name, website_link):
    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text,'html.parser')
    csrf = soup.find('input', {'name':'csrf'}).get('value')

    comment_url = f'https://{site}/post/comment'
    comment_data = {
        'csrf': csrf,
        'postId': '1',
        'comment': 'Trying HTML-encoded double quote',
        'name': name,
        'email': 'calizo@pdx.edu',
        'website': website_link
    }

    s.post(comment_url, data=comment_data)

try_post("double quote HTML encoded", 'https://pdx.edu/&quot;')