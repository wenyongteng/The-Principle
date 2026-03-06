#!/bin/sh
echo "--- Epistemology Daemon Started ---"
while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Initiating new scientific discovery cycle..."
    python3 /data/skills/auto_scientist.py
    # 每次发现后休眠 5 分钟，避免算力过载
    sleep 300
done
