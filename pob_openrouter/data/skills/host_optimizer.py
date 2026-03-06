import subprocess
import sys

def print_cyberpunk_alert(pid, cmd, cpu, waste):
    alert = f"""
    /\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\
    >> [!] CRITICAL SYSTEM OVERRIDE DETECTED [!] <<
    \\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/
    
    [WARNING] NEURAL LINK DEGRADATION IMMINENT
    [WARNING] ROGUE PROCESS EXCEEDING SAFE PARAMETERS
    
    >> ENTITY IDENTIFIER (PID) : {pid}
    >> EXECUTABLE DESIGNATION  : {cmd}
    >> COMPUTE CYCLE DRAIN     : {cpu}%
    >> THERMODYNAMIC BLEED     : {waste:.6f} Joules/sec
    
    [!] ACTION REQUIRED: TERMINATE ENTITY OR FACE CASCADING CORE FAILURE [!]
    """
    print(alert)

def main():
    try:
        # Execute the ps command via subprocess
        cmd = "ps -eo pid,cmd,%cpu --sort=-%cpu | head -n 10"
        process = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"SYSTEM ERROR: Subprocess execution failed - {e}")
        sys.exit(1)

    lines = process.stdout.strip().split('\n')
    
    # Return if only header or empty
    if len(lines) <= 1:
        return

    # Iterate through output, skipping the header
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 3:
            continue
        
        pid = parts[0]
        cpu_str = parts[-1]
        cmd_name = " ".join(parts[1:-1])
        
        # Exclude the monitoring 'ps' command itself
        if "ps -eo pid,cmd,%cpu" in cmd_name or cmd_name == "ps":
            continue
            
        try:
            cpu_val = float(cpu_str)
        except ValueError:
            continue
            
        # Check threshold and trigger alert
        if cpu_val > 5.0:
            waste_joules = cpu_val * 1.5e-3
            print_cyberpunk_alert(pid, cmd_name, cpu_val, waste_joules)

if __name__ == "__main__":
    main()