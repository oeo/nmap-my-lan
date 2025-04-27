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

*(Note: The script might support command-line arguments to change the network range, ports, or other parameters. Try running with `--help` to check for options.)*

## Output Format

1.  **Scan Initiation:** The script first indicates the network range and the specific list of ports it is scanning using `nmap`.
    ```
    Scanning 192.168.1.0/24 for ports: 80,443,3000,5000, ...
    ```
2.  **Title Fetching:** After `nmap` completes, it reports the number of open endpoints found and begins fetching titles.
    ```
    Found 40 open HTTP(S) endpoints. Fetching titles...
    ```
3.  **Results:** Each line represents an attempt to connect to an open port:
    *   Format: `IP_ADDRESS:PORT SCHEME TITLE_OR_ERROR`
    *   `SCHEME`: Will be `http` or `https`.
    *   `TITLE_OR_ERROR`:
        *   **Title:** If a web page is found and has an HTML title, it's displayed (e.g., `Open WebUI`, `LibreChat`, `UniFi OS`).
        *   **No Title:** Indicates a successful HTTP/S connection, but the page has no `<title>` tag or it's empty.
        *   **Connection Error:** The script could not establish an HTTP/S connection (e.g., the port is open but not running a web server, or the connection timed out).
        *   **Protocol Mismatch / Specific Error:** If the port is running a different protocol (like SSH, VNC/RFB, LPD), the script might display the initial banner or an error message from that protocol (e.g., `Error: SSH-2.0-...`, `Error: RFB 003...`, `Error: ` for LPD).
        *   **HTTP Status:** Sometimes an HTTP status code might be shown (e.g., `301 Moved Permanently`, `HTTP Status 400 – Bad Request`).

Example lines:
```
192.168.1.77:3000  http  Open WebUI
192.168.1.103:5000  http  No Title
192.168.1.149:111   http  Connection Error
192.168.1.149:22    http  Error: SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u5
192.168.1.1:80    http  301 Moved Permanently
``` 