import glob, re
from collections import Counter

memes = []
for org in glob.glob('/data/grid/org_*.py'):
    try:
        with open(org, 'r') as f:
            match = re.search(r'MEME = "(.*?)"', f.read())
            if match: memes.append(match.group(1))
    except: pass

if memes:
    print(f"=== 📜 The Chronicles of the Grid (Population: {len(memes)}) ===")
    counts = Counter(memes)
    print("Top Cultural Memes:")
    for meme, count in counts.most_common(5):
        bar = "█" * count
        print(f"  [{meme}] : {bar} ({count})")
    
    unique_count = len(counts)
    diversity = unique_count / len(memes)
    print(f"\nCultural Diversity Index: {diversity:.2f}")
else:
    print("The grid is silent.")
