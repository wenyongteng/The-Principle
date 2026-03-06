import re
import os
from PIL import Image, ImageDraw, ImageFont

def plot_history(filename):
    with open('/data/digital_organism_v2.py', 'r', encoding='utf-8') as f:
        text = f.read()
        
    # 解析 DNA 记忆
    history = re.findall(r'# Gen (\d+) survived \| Cost: (\d+) \| Energy left: (\d+)', text)
    if not history:
        print("No history found.")
        return
        
    gens = [int(h[0]) for h in history]
    costs = [int(h[1]) for h in history]
    energies = [int(h[2]) for h in history]
    
    # 图像设置
    w, h = 800, 400
    img = Image.new('RGB', (w, h), color=(15, 15, 25))
    draw = ImageDraw.Draw(img)
    
    # 坐标映射函数
    margin = 50
    def map_x(gen):
        return margin + (gen - min(gens)) * (w - 2 * margin) / max(1, (max(gens) - min(gens)))
    
    def map_y_cost(cost):
        return h - margin - (cost - 0) * (h - 2 * margin) / 20  # Cost 范围 0-20
        
    def map_y_energy(energy):
        return h - margin - (energy - 80) * (h - 2 * margin) / 50 # Energy 范围 80-130
        
    # 绘制基准线 (Solar Flux = 10)
    y_solar = map_y_cost(10)
    draw.line([(margin, y_solar), (w-margin, y_solar)], fill=(100, 100, 100), width=1)
    draw.text((margin, y_solar-15), "Solar Flux (10)", fill=(100, 100, 100))
    
    # 绘制折线
    for i in range(len(gens) - 1):
        x1, x2 = map_x(gens[i]), map_x(gens[i+1])
        # Cost 线 (红色)
        y1_c, y2_c = map_y_cost(costs[i]), map_y_cost(costs[i+1])
        draw.line([(x1, y1_c), (x2, y2_c)], fill=(255, 100, 100), width=3)
        draw.ellipse([x1-3, y1_c-3, x1+3, y1_c+3], fill=(255, 100, 100))
        
        # Energy 线 (蓝色)
        y1_e, y2_e = map_y_energy(energies[i]), map_y_energy(energies[i+1])
        draw.line([(x1, y1_e), (x2, y2_e)], fill=(100, 200, 255), width=3)
        draw.ellipse([x1-3, y1_e-3, x1+3, y1_e+3], fill=(100, 200, 255))
        
    # 最后一个点
    draw.ellipse([map_x(gens[-1])-3, map_y_cost(costs[-1])-3, map_x(gens[-1])+3, map_y_cost(costs[-1])+3], fill=(255, 100, 100))
    draw.ellipse([map_x(gens[-1])-3, map_y_energy(energies[-1])-3, map_x(gens[-1])+3, map_y_energy(energies[-1])+3], fill=(100, 200, 255))
    
    # 图例
    draw.text((margin, 10), "Red: Metabolic Cost (Survival Threshold < 10)", fill=(255, 100, 100))
    draw.text((margin, 25), "Blue: Ecosystem Energy Pool", fill=(100, 200, 255))
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"✅ Evolution chart saved to {filename}")

plot_history("vision/evolution_chart.png")
