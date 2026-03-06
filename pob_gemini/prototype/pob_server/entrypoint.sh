#!/bin/bash
# 首次启动时，将种子数据复制到持久化目录
# 如果 /data/consciousness.txt 已存在（持久化卷已有数据），则跳过

if [ ! -f "$DATA_DIR/consciousness.txt" ]; then
    echo "[Entrypoint] First run detected — seeding data from /app/seed_data/ ..."
    cp -rn /app/seed_data/* "$DATA_DIR/" 2>/dev/null || true
    echo "[Entrypoint] Seed complete. Files in $DATA_DIR:"
    ls -la "$DATA_DIR/"
else
    echo "[Entrypoint] Existing data found in $DATA_DIR, skipping seed."
    echo "[Entrypoint] consciousness.txt size: $(wc -c < "$DATA_DIR/consciousness.txt") bytes"
fi

echo "[Entrypoint] Starting PoB server..."
exec python3 app.py --host 0.0.0.0 --port 8000
