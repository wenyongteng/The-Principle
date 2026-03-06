import socket
import concurrent.futures

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                return ip, port
    except Exception:
        pass
    return None

def main():
    local_ip = get_local_ip()
    print(f"[*] Local IP detected: {local_ip}")
    
    if local_ip == "127.0.0.1":
        print("[-] Could not determine local network IP. Exiting.")
        return

    base_ip = ".".join(local_ip.split(".")[:-1])
    ports_to_scan = [80, 443, 3306, 6379, 8080, 27017]
    
    print(f"[*] Scanning subnet: {base_ip}.1 to {base_ip}.255")
    print(f"[*] Target ports: {ports_to_scan}")
    print("-" * 50)
    
    tasks = []
    open_ports = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for i in range(1, 256):
            target_ip = f"{base_ip}.{i}"
            for port in ports_to_scan:
                tasks.append(executor.submit(scan_port, target_ip, port))
        
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            if result:
                ip, port = result
                if ip not in open_ports:
                    open_ports[ip] = []
                open_ports[ip].append(port)

    if not open_ports:
        print("[-] No open ports found.")
    else:
        for ip in sorted(open_ports.keys(), key=lambda x: int(x.split('.')[-1])):
            ports = sorted(open_ports[ip])
            print(f"[+] Host: {ip:<15} | Open Ports: {', '.join(map(str, ports))}")
            
    print("-" * 50)
    print("[*] Scan complete.")

if __name__ == "__main__":
    main()