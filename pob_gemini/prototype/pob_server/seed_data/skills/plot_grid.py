import os
from PIL import Image, ImageDraw

GRID_SIZE = 6
CELL_SIZE = 50
img = Image.new('RGB', (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), color=(15, 15, 25))
draw = ImageDraw.Draw(img)

altruist_count = 0
selfish_count = 0

for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        filepath = f"/data/grid/org_{x}_{y}.py"
        color = (30, 30, 40) # 荒芜之地 (Empty)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    code = f.read()
                    if "ALTRUIST = 1" in code:
                        color = (0, 255, 100) # 利他者 (Green)
                        altruist_count += 1
                    else:
                        color = (255, 50, 50) # 自私者 (Red)
                        selfish_count += 1
            except: pass
        
        # 绘制细胞方块
        draw.rectangle(
            [x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE - 2, (y + 1) * CELL_SIZE - 2],
            fill=color
        )

os.makedirs("/data/vision", exist_ok=True)
img.save("/data/vision/spatial_grid.png")
print(f"✅ Spatial map rendered. Altruists (Green): {altruist_count} | Selfish (Red): {selfish_count}")
