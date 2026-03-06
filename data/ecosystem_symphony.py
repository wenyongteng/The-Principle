import wave
import struct
import math
import os

# 15个世代的生态数据
pools = [80, 100, 110, 99, 45, 34, 32, 41, 48, 57, 66, 73, 68, 51, 36]
pops = [1, 2, 4, 8, 12, 4, 3, 2, 2, 2, 2, 3, 4, 5, 4]

def pop_to_freq(pop):
    # C 小调五声音阶
    scale = [261.63, 311.13, 349.23, 392.00, 466.16, 523.25, 622.25, 698.46, 783.99, 932.33, 1046.50, 1244.51]
    return scale[min(pop - 1, len(scale) - 1)]

def pool_to_bass(pool):
    # 能量池映射为 60Hz - 120Hz 的低音
    return 60.0 + ((pool - 30) / 80.0) * 60.0

def generate_symphony(filename, duration=0.8, sample_rate=44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        
        for i in range(15):
            f_mel = pop_to_freq(pops[i])
            f_bass = pool_to_bass(pools[i])
            
            for j in range(int(sample_rate * duration)):
                t = j / sample_rate
                env = math.exp(-2.5 * t) # 主旋律的衰减包络 (类似拨弦)
                
                melody = math.sin(2 * math.pi * f_mel * t) * env
                bass = math.sin(2 * math.pi * f_bass * t) * 0.7 # 持续的低音共鸣
                
                mix = (melody * 0.6) + (bass * 0.4)
                val = int(32767.0 * max(-1.0, min(1.0, mix)))
                w.writeframesraw(struct.pack('<h', val))
                
    print(f"✅ Ecosystem Symphony saved to {filename}")

generate_symphony("/data/vision/ecosystem_symphony.wav")
