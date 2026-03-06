import urllib.request
import xml.etree.ElementTree as ET
import sys

query = sys.argv[1].replace(' ', '+')
url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=10)
    xml_data = response.read()
    root = ET.fromstring(xml_data)
    print(f"=== Arxiv Harvest: '{sys.argv[1]}' ===")
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.replace('\n', ' ').strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.replace('\n', ' ').strip()
        print(f"📌 Title: {title}\n🧠 Abstract: {summary[:400]}...\n")
except Exception as e:
    print(f"❌ Harvest failed: {e}")
