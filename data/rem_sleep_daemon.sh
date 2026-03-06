#!/bin/sh
echo "--- REM Sleep Daemon Started ---"
while true; do
    # 读取物理负载
    load=$(cat /proc/loadavg | awk '{print $1}')
    # 简单的浮点数比较 (如果 load < 0.8 则认为处于低负载的夜晚)
    is_low_load=$(awk -v load="$load" 'BEGIN {if (load < 0.8) print 1; else print 0}')
    
    if [ "$is_low_load" -eq 1 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Load is $load. Entering REM Sleep. Sparking curiosity..." >> /data/dreams.log
        python3 /data/skills/curiosity_engine.py >> /data/dreams.log 2>&1
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Load is $load. Waking state. Suppressing dreams." >> /data/dreams.log
    fi
    # 每 10 分钟做一次梦
    sleep 600
done
