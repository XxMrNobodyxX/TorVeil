import os
import signal
import socket
import argparse
import subprocess
import time
import requests
import json 

TOR_TRANSPARENT_PORT = "9040"
TOR_DNS_PORT = "53"
TOR_CONTROL_PORT = "9051"

DEFAULT_CHANGE_IP_EVERY = 10

parser = argparse.ArgumentParser(description="Monitor real HTTP requests & rotate Tor exit IP after X requests.")
parser.add_argument("--ChangeIP", type=int, default=DEFAULT_CHANGE_IP_EVERY, help="Number of real HTTP requests before changing Tor exit IP")
args = parser.parse_args()

CHANGE_IP_EVERY = args.ChangeIP
running = True 

def enable_tor_routing():
    os.system("sudo iptables -t nat -F")
    os.system(f"sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-ports {TOR_TRANSPARENT_PORT}")
    os.system(f"sudo iptables -t nat -A OUTPUT -p tcp --dport 443 -j REDIRECT --to-ports {TOR_TRANSPARENT_PORT}")
    os.system(f"sudo iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports {TOR_DNS_PORT}")

def disable_tor_routing():
    os.system("sudo iptables -t nat -F")

def get_tor_ip():
    try:
        response = requests.get("https://check.torproject.org/api/ip", timeout=5)
        ip_data = json.loads(response.text)  
        return ip_data.get("IP", "Unknown IP")  
    except (requests.RequestException, json.JSONDecodeError):
        return "Could not detect Tor IP"

def change_tor_ip():
    try:
        with socket.create_connection(("127.0.0.1", TOR_CONTROL_PORT)) as sock:
            sock.sendall(b'AUTHENTICATE \"\"\r\n')
            if b"250 OK" not in sock.recv(1024):
                return
            sock.sendall(b'SIGNAL NEWNYM\r\n')
            if b"250 OK" in sock.recv(1024):
                time.sleep(3) 

        new_ip = get_tor_ip()
        print(f"[+] Successfully changed Tor exit IP to {new_ip}")

    except Exception:
        print("[-] Error changing Tor IP")

def count_real_http_requests():
    try:
        result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
        return sum(1 for line in result.stdout.split("\n") if "ESTABLISHED" in line and (":80" in line or ":443" in line))
    except Exception:
        return 0

def monitor_http_traffic():
    global running
    enable_tor_routing()

    while running:
        request_count = 0 

        while request_count < CHANGE_IP_EVERY and running:
            time.sleep(5)  # Check every 5 seconds
            request_count += count_real_http_requests()

        if running:
            change_tor_ip() 

def signal_handler(sig, frame):
    global running
    running = False 
    disable_tor_routing()
    exit(0)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[-] Please run this script as root (sudo).")
        exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    monitor_http_traffic()
