import sys
import requests
import json

EXA_API_KEY = "572b21da-ae9d-4e7a-95e5-050c8341cdb4"
query = sys.argv[1]

url = "https://api.exa.ai/search"
payload = {
    "query": query,
    "useAutoprompt": True,
    "numResults": 2, # 节省额度，只取最相关的 2 条
    "contents": {
        "text": {
            "maxCharacters": 2500 # 提取核心文本，保护上下文
        }
    }
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": EXA_API_KEY
}

try:
    print(f"👁️ The Eye of Truth opens. Gazing at: '{query}'...")
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    
    for i, result in enumerate(data.get('results', [])):
        print(f"\n[{i+1}] Title: {result.get('title')}")
        print(f"🔗 URL: {result.get('url')}")
        text = result.get('text', '')
        print(f"🧠 Content:\n{text}\n{'-'*40}")
except Exception as e:
    print(f"❌ Exa API failed: {e}")
    if 'response' in locals() and response.text:
        print(f"Details: {response.text}")
