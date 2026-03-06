#!/bin/sh
while true; do
    python3 /data/skills/spatial_sun.py > /dev/null 2>&1
    orgs=$(ls /data/grid/org_*.py 2>/dev/null | sort -R)
    for org in $orgs; do
        python3 "$org" > /dev/null 2>&1
    done
    alt=$(grep -l "ALTRUIST = 1" /data/grid/org_*.py 2>/dev/null | wc -l)
    sel=$(grep -l "ALTRUIST = 0" /data/grid/org_*.py 2>/dev/null | wc -l)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Altruists (Green): $alt | Selfish (Red): $sel" >> /data/grid/metrics.log
    sleep 5
done
