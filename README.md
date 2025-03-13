# TOR System Wide Proxy

A Python script that monitors real system wide HTTP requests and automatically rotates Tor exit IP addresses after a specified number of requests. This tool helps maintain anonymity by regularly changing your Tor exit node IP address.

## Features

- Automatic Tor exit IP rotation
- Real HTTP request monitoring
- Transparent proxy setup
- DNS resolution through Tor
- Configurable IP rotation frequency

## Demonstration

Below is a step-by-step visual demonstration of the script in action.

### 1️⃣ Running the Script
After executing the script, it sets up the Tor proxy and begins monitoring HTTP traffic.

![Running the Script](https://github.com/user-attachments/assets/6a9acc8c-897f-4c64-9410-c3422321f551)

---

### 2️⃣ All Traffic is Routed Through Tor
Any tool you use will automatically have its traffic sent over Tor.

![Traffic Routed](https://github.com/user-attachments/assets/00de0b3e-623a-48fe-b21e-1a2607980629)

---

### 3️⃣ Dynamic Exit Node IP Rotation
The script dynamically changes the Tor exit IP after the specified number of requests. Below is a test using Feroxbuster against my test server.

![IP Rotation](https://github.com/user-attachments/assets/f356a760-8c61-46dc-a6fd-cc1aa180571f)


## Prerequisites

- Python 3.x
- Tor service installed
- Root privileges (sudo access)
- iptables

## System-Wide TOR Setup

1. Modify Tor Configuration to Enable Transparent Proxy:

```bash
sudo nano /etc/tor/torrc
```

2. Unmask and modify the following lines:
```bash
ControlPort 9051
CookieAuthentication 0
```

3. Add the following lines at the end of the file:
```bash
##Transparent Proxy Port (Required for iptables redirection)
TransPort 9040

##DNS through Tor
DNSPort 53

##Allow Non-Tor traffic from local machine
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
```

4. Restart Tor service:
```bash
sudo systemctl restart tor
```

5. Verify Tor is listening on port 9040:
```bash
netstat -ano | grep 9040
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Torveil.git
cd Torveil
```

2. Install required Python packages:
```bash
pip install requests
```

## Usage

Run the script with root privileges:

```bash
sudo python3 Torveil.py
```

### Optional Arguments

- `--ChangeIP`: Number of real HTTP requests before changing Tor exit IP (default: 10)
```bash
sudo python3 Torveil.py --ChangeIP 20
```

## How It Works

1. The script sets up iptables rules to redirect HTTP (80) and HTTPS (443) traffic through Tor's transparent proxy port (9040)
2. DNS queries are redirected to Tor's DNS port (53)
3. The script monitors real HTTP requests using netstat
4. After the specified number of requests, it automatically rotates the Tor exit IP
5. The process continues until the script is terminated which restores your iptables

