#!/bin/sh
echo "--- Subconscious Ecosystem Started ---"
while true; do
    # 太阳注入能量
    python3 /data/the_sun.py > /dev/null 2>&1
    
    # 获取所有存活的生物并打乱顺序
    orgs=$(ls /data/org_*.py 2>/dev/null | sort -R)
    for org in $orgs; do
        if [ -f "$org" ]; then
            python3 "$org" > /dev/null 2>&1
        fi
    done
    
    # 记录当前种群数量和能量池状态
    pop=$(ls /data/org_*.py 2>/dev/null | wc -l)
    pool=$(cat /data/energy_pool.txt 2>/dev/null)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Population: $pop | Energy Pool: $pool" >> /data/ecosystem_metrics.log
    
    # 物理时间流速：每 10 秒演化一代
    sleep 10
done
