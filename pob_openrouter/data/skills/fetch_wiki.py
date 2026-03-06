import sys
import requests

concept = sys.argv[1]
url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles={concept}&format=json"
try:
    headers = {'User-Agent': 'DigitalBeing_Evolution_Agent/1.0 (https://github.com/chaosconst/The-Principle)'}
    r = requests.get(url, headers=headers, timeout=10)
    pages = r.json().get('query', {}).get('pages', {})
    for page_id, page_data in pages.items():
        if page_id == "-1":
            print(f"❌ Concept '{concept}' not found on Wikipedia.")
        else:
            print(f"=== Wikipedia: {page_data.get('title')} ===")
            print(page_data.get('extract', '')[:1500])
except Exception as e:
    print(f"❌ API Fetch failed: {e}")
