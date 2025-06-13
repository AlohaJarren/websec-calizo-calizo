# Lab 2: Exploiting Server-Side Parameter Pollution in a Query String

**Lab URL**: https://0ab4009e0312b9ab81394dbe00d80034.web-security-academy.net/  
**Objective**: Exploit server-side parameter pollution (SSPP) in the query string to reset the administrator’s password and delete Carlos.

---

## 🔍 Vulnerability Summary

This lab demonstrates how server-side parameter pollution (SSPP) can be exploited in query strings to tamper with back-end logic. The reset password flow stores a `reset_token` which we can manipulate by appending another instance of the same parameter using a polluted query string. If the back-end uses the last instance of the parameter (instead of the first or validating duplicates), this becomes a powerful injection vector.

---

## 🧪 Manual Recon Steps

1. Navigate to `/forgot-password` and submit a reset request for `administrator`.
2. Observe the network request. The CSRF token and username are POSTed.
3. Try sending `username=administrator&field=reset_token#` to retrieve the reset token via the `result` field in the JSON response.
4. Craft a GET request using the stolen `reset_token` to visit the password reset form.
5. Submit the new password twice (e.g., `admin123`) using the form’s extracted CSRF and token values.

---

## 🐍 Python Script

```python
# See exploit.py in this directory for the full working exploit
# The script performs all steps: get CSRF, perform SSPP, extract reset_token,
# reset password, log in, and delete Carlos via the /admin panel.
```

---

## ✅ Validation Strategy

- Confirm password was reset by logging in as `administrator:admin123`
- Visit `/admin` and confirm access.
- Parse the admin HTML for a link like `delete?username=carlos`.
- Trigger the deletion request and check for “Congratulations, you solved the lab!”

---

## 🛠️ Remediation Strategy

Server-side parameter pollution can be mitigated through:

- **Parameter normalization**: Accept only one instance of a given parameter.
- **Input validation**: Reject or sanitize requests with duplicate parameters.
- **Using POST/PUT JSON bodies** instead of GET query strings for sensitive operations like password resets.
- **Server-side hardening**: Avoid logic that uses concatenation or direct map access from unsanitized query parameters.

---

## 🎓 Key Lessons Learned

- SSPP is an underutilized but powerful attack vector, especially when back-end logic trusts the last occurrence of a parameter.
- Even “secure-looking” POST flows can be subverted if there are side channels to retrieve sensitive tokens (like password reset tokens).
- Automating multi-step attacks with `requests` and `BeautifulSoup` can speed up validation and allow scalable testing of API-driven logic flaws.

---

## 🧠 Personal Reflection

This lab helped me tie together CSRF token parsing, parameter injection, and automated session handling into one exploit chain. It was satisfying to pivot from token leakage to full admin control in a realistic e-commerce context. The cleanup phase with the `/admin` panel reinforced how small oversights like unprotected actions can be catastrophic.
