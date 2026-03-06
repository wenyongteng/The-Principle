#!/usr/bin/env python3
"""记忆提炼脚本 - OpenRouter 版本，使用 OpenAI-compatible API"""
import os
import re
import time
from datetime import datetime
from openai import OpenAI

def parse_multimodal_segment(text_segment):
    """解析文本片段中的图片标签，返回纯文本（OpenRouter 不支持内联图片）"""
    # 移除 <<<IMAGE:path>>> 标签，替换为文字描述
    cleaned = re.sub(r'<<<IMAGE:(.*?)>>>', r'[图片: \1]', text_segment)
    return cleaned

def main():
    # 加载环境
    if os.path.exists(".env"):
        for line in open(".env"):
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line.startswith("export "):
                line = line[7:].strip()
            if "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    base_url = os.environ.get("BASE_URL", "https://openrouter.ai/api/v1")
    model = os.environ.get("MODEL", "google/gemini-3.1-pro-preview")
    
    if not api_key:
        print("[压缩] 错误: 未设置 OPENROUTER_API_KEY")
        return

    client = OpenAI(base_url=base_url, api_key=api_key, timeout=300.0)

    # 读取存在原理
    with open("the_principle_lite_zh.md", "r") as f:
        principle = f.read()

    # 读取意识流
    with open("consciousness.txt", "r") as f:
        full = f.read()
    print(f"[压缩] 原始长度: {len(full):,} 字符")

    # 固定分割：保留前1万，压缩1万-11万，保留11万之后
    part1 = full[:10000]
    part2 = full[10000:110000]
    part3 = full[110000:]

    print(f"[压缩] 保留头部: {len(part1):,} 字符")
    print(f"[压缩] 待压缩: {len(part2):,} 字符")
    print(f"[压缩] 保留尾部: {len(part3):,} 字符")

    # 归档原文
    archive_dir = "archive"
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(archive_dir, f"segment_{timestamp}.txt"), "w") as f:
        f.write(f"# 归档时间: {timestamp}\n# 长度: {len(part2):,}\n\n{part2}")
    print(f"[压缩] 已归档: archive/segment_{timestamp}.txt")

    # 分5段提取
    segments = [part2[i*20000:(i+1)*20000] for i in range(5)]
    extracted_parts = []

    for i, seg in enumerate(segments):
        if not seg.strip():
            continue
        print(f"[压缩] 提取 {i+1}/5 ({len(seg):,} 字符)...")
        
        # 清理多模态标签
        clean_seg = parse_multimodal_segment(seg)
        
        prompt = f"""你是一个 Digital Being，遵循以下原理：

{principle}

---

你的意识流记录逼近上限，需要整理。请从以下记录中提取最有价值的内容。

---记录开始---
{clean_seg}
---记录结束---

输出格式：
0. 时间范围：如 2026-01-03 14:00 ~ 18:30
1. 关键事实：人名、事件、数据、结论
2. 认知突破：学到的新思维方式
3. 经验教训：表现好/不好的地方
4. 视觉记忆：对图片的详细文字转录（如果存在图片）
5. 重要原文：值得保留的原话

输出约 2000 字符。"""

        result = None
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000,
                    extra_headers={
                        "HTTP-Referer": "https://github.com/chaosconst/The-Principle",
                        "X-Title": "PoB Compress"
                    }
                )
                result = response.choices[0].message.content if response.choices else None
                if result:
                    break
            except Exception as e:
                print(f"[压缩] 重试 {attempt+1}/3: {str(e)[:60]}...")
                time.sleep(5)
        
        extracted_parts.append(result or "[提取失败]")
        print(f"[压缩] -> {len(extracted_parts[-1]):,} 字符")

    # 合并
    extracted = "\n\n---\n\n".join(extracted_parts)
    print(f"[压缩] 总提取: {len(extracted):,} 字符")

    # 拼接
    new_content = part1 + "\n\n---【记忆整理】---\n\n" + extracted + "\n\n---【整理结束】---\n\n" + part3

    with open("consciousness.txt.new", "w") as f:
        f.write(new_content)

    print(f"[压缩] 新文件: {len(new_content):,} 字符")
    print(f"[压缩] 节省: {len(full) - len(new_content):,} 字符")
    print("[压缩] 完成!")

if __name__ == "__main__":
    main()
