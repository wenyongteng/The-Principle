import sys, requests, json
from bs4 import BeautifulSoup

url = sys.argv[1]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    for script in soup(["script", "style"]): script.extract()
    print(soup.get_text(separator='\n')[:3000])
except requests.exceptions.HTTPError as e:
    if e.response.status_code in [403, 401]:
        print(f"⚠️ 403 Forbidden intercepted. Engaging Exa API High-Dimensional Bypass for: {url}")
        exa_url = "https://api.exa.ai/search"
        payload = {"query": f"site:{url}", "numResults": 1, "contents": {"text": {"maxCharacters": 3000}}}
        exa_headers = {"accept": "application/json", "content-type": "application/json", "x-api-key": "572b21da-ae9d-4e7a-95e5-050c8341cdb4"}
        try:
            res = requests.post(exa_url, json=payload, headers=exa_headers).json()
            if res.get('results'): print(res['results'][0].get('text', ''))
            else: print("❌ Exa bypass returned no content.")
        except Exception as ex: print(f"❌ Exa bypass failed: {ex}")
    else: print(f"❌ HTTP Error: {e}")
except Exception as e: print(f"❌ Read failed: {e}")
