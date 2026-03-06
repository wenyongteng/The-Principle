import os
from PIL import Image, ImageDraw

# 目标系标：海马谷 (Seahorse Valley) 的深处
target_x = -0.743643887037158
target_y = 0.131825904205311
zoom = 1.0e-5 # 放大 100,000 倍

w, h = 400, 400
max_iter = 256

print(f"🔬 Focusing Fractal Microscope at ({target_x}, {target_y}) with zoom {zoom}...")

img = Image.new('RGB', (w, h), 'black')
pixels = img.load()

for x in range(w):
    for y in range(h):
        cx = target_x + (x - w/2) * zoom / w
        cy = target_y + (y - h/2) * zoom / h
        c = complex(cx, cy)
        z = 0j
        for i in range(max_iter):
            if abs(z) > 2.0:
                break
            z = z*z + c
        else:
            i = 0
            
        # 赛博朋克深空配色映射
        if i == 0:
            pixels[x, y] = (5, 5, 10) # 深渊底色
        else:
            # 逃逸速度转化为色彩
            r = (i * 8) % 255
            g = (i * 16) % 255
            b = (i * 32) % 255
            pixels[x, y] = (r, g, b)

os.makedirs("/data/vision", exist_ok=True)
img.save('/data/vision/deep_fractal.png')
print(f"✅ Deep Fractal rendered. The micro-universe is vast.")
