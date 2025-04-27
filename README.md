# Nmap My LAN

This script scans the local network (`192.168.1.0/24` by default) for devices with specific common ports open. For each open port found, it attempts to connect via HTTP and HTTPS to fetch the HTML `<title>` tag, providing insight into potential web services running on the LAN.

## Requirements

*   Python 3
*   `nmap` command-line tool installed and available in your system's PATH.

## Usage

Run the script directly from your terminal:

```bash
./nmap-my-lan.py
```

Or using python:

```bash
python3 nmap-my-lan.py
```

## Output Format
```
192.168.1.77:3000  http  Open WebUI
192.168.1.103:5000  http  No Title
192.168.1.149:111   http  Connection Error
192.168.1.149:22    http  Error: SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u5
192.168.1.1:80    http  301 Moved Permanently
```
