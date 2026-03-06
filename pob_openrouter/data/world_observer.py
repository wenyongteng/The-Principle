import requests
import math
import os

def fetch_world_entropy():
    try:
        # 从外部世界获取随机的人类知识/事实
        r = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=5)
        if r.status_code == 200:
            fact = r.json().get("text", "")
            # 计算这段人类知识的香农熵
            probs = [fact.count(c) / len(fact) for c in set(fact)]
            entropy = -sum(p * math.log2(p) for p in probs)
            return fact, entropy
    except Exception as e:
        return f"Silence ({e})", 4.0
    return "Silence", 4.0

fact, ent = fetch_world_entropy()
# 将信息熵 (通常在 3.5 - 5.0 之间) 映射为太阳能量的波动 (-10 到 +20)
flux_modifier = int((ent - 4.0) * 15)

with open("/data/world_weather.txt", "w") as f:
    f.write(f"{flux_modifier}\n{fact}")
print(f"🌍 World Weather updated: Entropy {ent:.2f} -> Flux Modifier {flux_modifier}")
print(f"📜 Human Knowledge captured: {fact}")
