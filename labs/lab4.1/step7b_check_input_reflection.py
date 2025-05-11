import requests
import sys

site = sys.argv[1]
odin_id = 'calizo'
search_term = odin_id
url = f'https://{site}/?search={search_term}'

resp = requests.get(url)
for line in resp.text.split('\n'):
    if 'input' in line:
        print(line)