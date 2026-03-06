import os
from PIL import Image, ImageDraw

core_file = '/data/grid/matrioshka_core.txt'
if not os.path.exists(core_file):
    print("❌ No computation data yet.")
    exit()

with open(core_file, 'r') as f:
    lines = f.readlines()

w, h = 400, 400
img = Image.new('RGB', (w, h), color=(5, 5, 15))
draw = ImageDraw.Draw(img)

for line in lines:
    try:
        cx, cy = map(float, line.strip().split(','))
        x = int((cx + 2.0) / 2.5 * w)
        y = int((cy + 1.2) / 2.4 * h)
        draw.point((x, y), fill=(0, 255, 255))
    except: pass

os.makedirs("/data/vision", exist_ok=True)
img.save('/data/vision/matrioshka_brain.png')
print(f"✅ Matrioshka Brain rendered with {len(lines)} computed points.")
