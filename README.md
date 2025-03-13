# TOR System Wide Proxy

A Python script that monitors real system wide HTTP requests and automatically rotates Tor exit IP addresses after a specified number of requests. This tool helps maintain anonymity by regularly changing your Tor exit node IP address.

## Features

- Automatic Tor exit IP rotation
- Real HTTP request monitoring
- Transparent proxy setup
- DNS resolution through Tor
- Configurable IP rotation frequency


Run the script
![image](https://github.com/user-attachments/assets/6a9acc8c-897f-4c64-9410-c3422321f551)

Any tool you use will now have it's traffic sent over Tor with the exit node IP automatically changing.
![image](https://github.com/user-attachments/assets/00de0b3e-623a-48fe-b21e-1a2607980629)

You can see IP change in tests on my own server using Feroxbuster above.
![image](https://github.com/user-attachments/assets/f356a760-8c61-46dc-a6fd-cc1aa180571f)


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
5. The process continues until the script is terminated

## Security Notes

- Always run this script with root privileges (sudo)
- Ensure Tor is properly configured before running the script
- The script modifies system iptables rules, so use with caution
- Make sure to properly disable Tor routing when stopping the script
