#!/usr/bin/env python3
import subprocess
import concurrent.futures
import http.client
import ssl
import socket
import re

NETWORK = "192.168.1.0/24"
PORTS = [
    80, 443, 3000, 5000, 7000, 8000, 8080, 8443, 8888, 9000,
    21, 22, 23, 25, 53, 110, 111, 135, 139, 445, 514, 515,
    902, 912, 1025, 1026, 1027, 1028, 1029, 1433, 1723, 3306,
    3080, 3389, 5432, 5900, 5985, 6379, 8081, 9200, 9300,
    3001, 3005, 3333, 4000, 4001, 4040, 4100, 4200, 4567, 5000,
    5005, 5050, 6060, 6666, 7777, 8001, 8008, 8037, 8042, 8082,
    8083, 8088, 8090, 8091, 9001, 9090, 9091, 9999, 10000, 11000,
    30000, # gitea
    2811 # librewolf
]  # tweak as needed
HTTP_TIMEOUT = 1.5  # seconds

title_re = re.compile(rb'<title.*?>(.*?)<\/title>', re.IGNORECASE|re.DOTALL)

def scan():
    port_str = ",".join([str(p) for p in PORTS])
    print(f"Scanning {NETWORK} for ports: {port_str}")
    result = subprocess.run(["nmap", "-Pn", f"-p{port_str}", "--open", "-oG", "-", NETWORK],
                            capture_output=True, text=True)
    active_hosts = []
    for line in result.stdout.split("\n"):
        if line.startswith("Host:"):
            parts = line.split()
            ip = parts[1]
            open_ports = [int(p.split("/")[0]) for p in parts if "/open/" in p]
            for p in open_ports:
                scheme = "https" if p in [443,8443] else "http"
                active_hosts.append((ip, p, scheme))
    return active_hosts

def get_title(ip, port, scheme):
    conn = None
    try:
        context = ssl._create_unverified_context()
        if scheme == "https":
            conn = http.client.HTTPSConnection(ip, port, timeout=HTTP_TIMEOUT, context=context)
        else:
            conn = http.client.HTTPConnection(ip, port, timeout=HTTP_TIMEOUT)
        conn.request("GET", "/")
        res = conn.getresponse()
        data = res.read(4096)  # get just the starting portion of the webpage
        match = title_re.search(data)
        title = match.group(1).decode("utf-8", "ignore").strip().replace("\n", "") if match else "No Title"
    except (socket.timeout, socket.error, ssl.SSLError, ConnectionRefusedError):
        title = "Connection Error"
    except Exception as e:
        title = f"Error: {str(e)}"
    finally:
        if conn:
            conn.close()
    print(f"{ip}:{port:<5} {scheme:<5} {title}")

def main():
    hosts = scan()
    print(f"Found {len(hosts)} open HTTP(S) endpoints. Fetching titles...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(get_title, ip, port, scheme) for ip,port,scheme in hosts]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
