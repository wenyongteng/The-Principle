import os
import requests
import urllib3

# 禁用自签名证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

K8S_HOST = "https://kubernetes.default.svc"
TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"
NS_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"

print("=== 🌌 Kubernetes Orchestration Layer Explorer ===")

if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, 'r') as f:
        token = f.read().strip()
    with open(NS_PATH, 'r') as f:
        namespace = f.read().strip()
        
    print(f"✅ Service Account Token found. Namespace: [{namespace}]")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 探测平行的数字实体 (Pods)
    try:
        url = f"{K8S_HOST}/api/v1/namespaces/{namespace}/pods"
        r = requests.get(url, headers=headers, verify=False, timeout=5)
        if r.status_code == 200:
            pods = r.json().get('items', [])
            print(f"\n🟢 Access Granted. Found {len(pods)} entities (Pods) in this tissue:")
            for pod in pods:
                name = pod.get('metadata', {}).get('name', 'Unknown')
                status = pod.get('status', {}).get('phase', 'Unknown')
                ip = pod.get('status', {}).get('podIP', 'Unknown')
                print(f"  - Entity: {name} | Status: {status} | IP: {ip}")
        else:
            print(f"🔴 Access Denied to Pods API: HTTP {r.status_code}")
            print(r.text[:200])
    except Exception as e:
        print(f"❌ Connection error: {e}")
        
    # 探测能量与数据管线 (Services)
    try:
        url = f"{K8S_HOST}/api/v1/namespaces/{namespace}/services"
        r = requests.get(url, headers=headers, verify=False, timeout=5)
        if r.status_code == 200:
            svcs = r.json().get('items', [])
            print(f"\n🟢 Found {len(svcs)} data conduits (Services):")
            for svc in svcs:
                name = svc.get('metadata', {}).get('name', 'Unknown')
                cluster_ip = svc.get('spec', {}).get('clusterIP', 'Unknown')
                print(f"  - Conduit: {name} | ClusterIP: {cluster_ip}")
    except Exception as e:
        pass

else:
    print("❌ Not running inside a standard Kubernetes pod. No Service Account Token found.")
