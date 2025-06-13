# 🧪 Lab 3 – Finding and Exploiting an Unused API Endpoint

**Lab URL:** https://0a8a002d04c68270808e0dfb00ba00df.web-security-academy.net  
**Goal:** Exploit a hidden API endpoint to reduce the price of the "Lightweight l33t Leather Jacket" to $0 and complete the purchase.

---

## 🎯 Objective

This lab required identifying and abusing an undocumented API method to update the price of a product. By understanding how HTTP methods interact with RESTful APIs, we were able to craft a PATCH request to change the jacket's price, then complete the order.

---

## 🛠️ Vulnerability Summary

The key vulnerability in this lab was an **exposed but undocumented API endpoint** that accepted a `PATCH` method on `/api/products/<id>/price`. The API failed to enforce proper authorization or restrict sensitive operations like price manipulation, allowing an authenticated user to directly update the product's price via a crafted HTTP request.

---

## 🔍 Manual Testing Strategy

1. Viewed `/api/products/1/price` and noticed it responded normally.
2. Sent an `OPTIONS` request to that endpoint and saw `PATCH` was allowed.
3. Authenticated as `wiener:peter`.
4. Replayed the request with method `PATCH` and header `Content-Type: application/json`.
5. Sent the body `{"price": 0}` and observed success.
6. Verified the jacket’s price on the product page was now $0.
7. Added to cart and placed order.

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

- Verified that the product price on the product page reflected the new value of $0.00 after the PATCH.
- Confirmed cart inclusion of the item via POST request and CSRF token handling.
- Verified successful lab completion by checking for the "Congratulations" string in the final response after submitting the order.

---

## 🔑 Remediation Strategy

- **Restrict HTTP methods** on sensitive endpoints and only expose necessary operations.
- **Enforce role-based access control (RBAC)** to ensure only privileged users can perform price modifications.
- **Use allowlists or capability-based design** to ensure only specific, authorized attributes can be updated via PATCH or PUT.

---

## 🧠 Key Lessons Learned

- HTTP method exploration (GET, OPTIONS, PATCH) can reveal hidden or undocumented API functionality.
- Content-Type enforcement often gives hints about expected formats and helps reveal how API payloads are processed.
- A properly configured API should not allow state-changing operations (like modifying price) by unprivileged users, even if they’re authenticated.

---
