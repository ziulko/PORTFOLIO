# Modular Honeypot (Python Version)

**Modular Honeypot** is a configurable honeypot written in **Python**, designed to detect suspicious network activity, log connections, and generate detailed session reports.

> ⚠ Note: This is the **Python version**. Implementations in other languages (e.g., C++, Go) are planned in the future.

---

## Features

* Monitor multiple ports (default, full, or custom)
* Optional **test mode** that simulates traffic
* Color-coded real-time logs in terminal (`LIVE`, `INFO`, `ERROR`)
* Session analysis includes:

  * Top source IPs
  * Activity by hour
  * Repeated request signatures
  * Detection of IPs scanning multiple ports
* Export reports to:

  * `.txt` (human readable)
  * `.json`
  * `.csv` (e.g., for Excel)
* Automatically organizes logs and reports by **date** and **session**

---

## Requirements

* Python 3.7+
* Operating system with socket support
* Admin privileges (if using ports <1024)

---

## Usage

### 1. Command-line Execution

```bash
python honeypot_python.py [mode] [--flags]
```

**Modes:**

* `default` → monitors default ports (21, 22, 23, 80, 443)
* `all` → monitors full range (1-65535)
* `<number>` → single custom port (e.g., `8888`)

**Examples:**

```bash
python honeypot_python.py default
python honeypot_python.py 8888 --test
python honeypot_python.py all --no-color
```

**Optional flags:**

* `--test` → run in test mode (simulate random pings)
* `--no-color` → disable terminal colors
* `--no-live` → disable live terminal output

### 2. Interactive Mode

Run without arguments to launch menu:

```
Choose port monitoring mode:
[1] Default ports (21, 22, 23, 80, 443)
[2] All ports (1-65535)
[3] Custom port (e.g. 8888)
[4] Default ports (TEST MODE)
```

---

## Folder Structure

```
honeypot_logs/
└── 2025-07-01/
    ├── port_21.log
    ├── port_22.log
    ├── ...
    └── reports/
        ├── session_summary_HH-MM-SS.txt
        ├── session_summary_HH-MM-SS.json
        └── session_summary_HH-MM-SS.csv
```

---

## Sample Report

```
Honeypot Session Report - 2025-07-01 19:12:10
Session started at: 2025-07-01 18:29:24
Session duration: 0h:42m:45s

[Port Activity]
Port 80 - 12 connections
Port 443 - 15 connections
...

[Top IP Addresses]
192.168.1.20: 5 connections
...

[Activity by Hour]
18:00 - 8 connections
19:00 - 19 connections

[Repeated Request Signatures]
'test-ping' - 34 times

[Potential Scanners]
192.168.1.77 scanned ports: [21, 22, 23, 80, 443]
```

---

## Test Mode

Use `--test` flag or menu option `[4]`. The program will simulate 5-20 random connections per port.

---

## Project Status

This project is under **active development** and serves as an educational prototype. Support for other languages and network behaviors may be added.

---

## Feedback

Suggestions and contributions are welcome! Create an issue or submit a pull request on GitHub.
