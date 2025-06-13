# 🔬 Lab 4: Exploiting a Mass Assignment Vulnerability

**Lab URL:** https://0a10004204dd913d839a737600aa0086.web-security-academy.net/

---

## 🎯 Objective

Exploit a mass assignment vulnerability to successfully purchase the _Lightweight l33t Leather Jacket_ despite having insufficient credit on the account. The solution requires tampering with a hidden parameter (`chosen_discount`) in a POST request to bypass authorization and force a 100% discount.

---

## 🧠 Vulnerability Summary

**Mass Assignment** occurs when server-side code automatically binds request data (like JSON or form fields) to internal objects without filtering or validating which properties are being modified. Attackers can use this to inject unauthorized or sensitive parameters (e.g., `isAdmin`, `discount`, `price`, etc.) that should not be client-controllable.

This lab leaks internal object structure via the GET `/api/checkout` response, which exposes a `chosen_discount` object not shown in the UI or original POST request. Exploiting this allows us to inject a 100% discount on the product and finalize the purchase.

---

## 🛠️ Exploitation Steps

1. **Login** with the provided credentials `wiener:peter`.

2. **Browse the Homepage** and locate the product ID for _Lightweight l33t Leather Jacket_.

3. **Add Product to Cart** and attempt checkout. The site denies the order due to insufficient funds.

4. **Capture API Requests** using Burp Suite. Observe both the GET and POST requests to `/api/checkout`.

5. **Discover Hidden Parameter:** The GET response reveals a `chosen_discount` object that’s not sent by the browser during checkout.

6. **Mass Assignment Attack:**

   - Modify the JSON in the POST request to inject the `chosen_discount` object.
   - Set the discount percentage to `100`.

7. **Send Modified Request** and observe a silent response. The server processes the transaction with the discount, solving the lab.

---

## 🐍 Python Script

```python
# See exploit.py in this directory for the full working exploit.
# The script logs in as wiener, locates the product ID of the "l33t" jacket,
# and performs a POST request to /api/checkout with a crafted chosen_discount
# field to exploit the mass assignment vulnerability and complete the purchase.
```

---

## 🧪 Validation Strategy

- **Lab Success Criteria:** Lab is considered solved when the l33t Leather Jacket is successfully purchased using a 100% discount.
- **Confirmation Clue:** The PortSwigger lab dashboard visually updates lab status after the API exploit completes.
- **Debug Observation:** The final POST request may not echo success in the response, but the lab is still marked solved. A silent success is typical in this lab.

---

## 🛡️ Remediation Strategy

- **Disable Dangerous Defaults:** Never use insecure object binding (e.g., Rails’ `params.permit!`, Express’ `req.body` object mutation) without filtering.
- **Allowlist Parameters:** Define strict schemas for expected inputs using tools like:
  - `pydantic` (Python)
  - `Joi` (Node.js)
  - `OpenAPI/Swagger` validation
- **Sanitize or Filter Request Data:** Ignore unknown fields not explicitly listed in your business logic.
- **Avoid Reflecting Sensitive Fields:** The inclusion of `chosen_discount` in a GET API response gave away the internal structure.
- **Regular API Audits:** Continuously test for unexpected parameter acceptance using static analysis or fuzzing tools.

---

## 📌 Key Lessons Learned

- Mass assignment can turn innocent UI actions into privilege escalation if backend object mapping is too trusting.
- Never assume that hidden fields in a GET response won’t be exploited — especially if JSON structures are mirrored in client-server exchanges.
- Effective exploitation often involves **parameter diffing**: comparing what’s sent vs. what’s accepted.
- Always validate backend logic independently of what’s shown to users in the UI.
