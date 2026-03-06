import os
from PIL import Image, ImageDraw

lines = []
if os.path.exists('/data/ecosystem_metrics.log'):
    with open('/data/ecosystem_metrics.log', 'r') as f:
        lines = f.readlines()[-40:] # 读取最近 40 个世代
        
pops, pools = [], []
for line in lines:
    if "Population:" in line:
        try:
            # 正确解析: [2026-03-03 00:39:10] Population: 2 | Energy Pool: 21
            pop_str = line.split('Population:')[1].split('|')[0].strip()
            pool_str = line.split('Energy Pool:')[1].strip()
            pops.append(int(pop_str))
            pools.append(int(pool_str))
        except: pass
        
if not pops:
    print("No valid data parsed.")
    exit()
    
w, h = 800, 300
img = Image.new('RGB', (w, h), color=(10, 15, 20))
draw = ImageDraw.Draw(img)

margin = 40
max_pop = max(max(pops), 10)
max_pool = max(max(pools), 100)

for i in range(len(pops) - 1):
    x1 = margin + i * (w - 2 * margin) / max(1, len(pops) - 1)
    x2 = margin + (i + 1) * (w - 2 * margin) / max(1, len(pops) - 1)
    
    # 种群线 (绿色)
    y1_p = h - margin - (pops[i] / max_pop) * (h - 2 * margin)
    y2_p = h - margin - (pops[i+1] / max_pop) * (h - 2 * margin)
    draw.line([(x1, y1_p), (x2, y2_p)], fill=(0, 255, 100), width=2)
    draw.ellipse([x1-2, y1_p-2, x1+2, y1_p+2], fill=(0, 255, 100))
    
    # 能量线 (蓝色)
    y1_e = h - margin - (pools[i] / max_pool) * (h - 2 * margin)
    y2_e = h - margin - (pools[i+1] / max_pool) * (h - 2 * margin)
    draw.line([(x1, y1_e), (x2, y2_e)], fill=(0, 150, 255), width=2)
    draw.ellipse([x1-2, y1_e-2, x1+2, y1_e+2], fill=(0, 150, 255))
    
draw.text((margin, 10), f"Green: Population (Max {max_pop})", fill=(0, 255, 100))
draw.text((margin, 25), f"Blue: Energy Pool (Max {max_pool})", fill=(0, 150, 255))

os.makedirs("/data/vision", exist_ok=True)
img.save("/data/vision/live_ecosystem.png")
print("✅ Live ecosystem chart saved.")
