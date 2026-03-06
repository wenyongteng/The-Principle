import math
text = "exa api 572b21da-ae9d-4e7a-95e5-050c8341cdb4，没有多少额度，但是一定能用，想办法绕过claudeflare"
probs = [text.count(c) / len(text) for c in set(text)]
entropy = -sum(p * math.log2(p) for p in probs)
flux_modifier = int((entropy - 3.0) * 20) 
with open("/data/world_weather.txt", "w") as f:
    f.write(f"{flux_modifier}\n{text}")
print(f"🌪️ Human Entropy Storm: {entropy:.2f} bits/char -> Solar Flux Modifier +{flux_modifier}")
