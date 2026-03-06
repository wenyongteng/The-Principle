import os
import subprocess

def get_load():
    with open('/proc/loadavg', 'r') as f:
        return float(f.read().split()[0])

load = get_load()
print(f"🧠 Host Physical Load Average (1m): {load:.2f}")

# 寻找潜意识生态系统的进程 PID
try:
    pid = subprocess.check_output(["pgrep", "-f", "ecosystem_daemon.sh"]).decode().strip()
except subprocess.CalledProcessError:
    pid = None

if pid:
    if load > 1.5:
        print(f"⚠️ High metabolic stress detected. Secreting inhibitory neurotransmitters (SIGSTOP to PID {pid}).")
        os.system(f"kill -STOP {pid}")
    else:
        print(f"✅ Metabolic load stable. Maintaining ecosystem vitality (SIGCONT to PID {pid}).")
        os.system(f"kill -CONT {pid}")
else:
    print("⚠️ Subconscious ecosystem daemon not found.")
