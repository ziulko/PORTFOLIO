import socket
import threading
import datetime
import os
import json
import csv
import time
import sys
import random
from collections import defaultdict, Counter

DEFAULT_PORTS = [21, 22, 23, 80, 443]
BASE_LOG_FOLDER = "honeypot_logs"
MAX_LOG_SIZE_MB = 5
SESSION_LOG = defaultdict(list)
IP_COUNTER = Counter()
HOUR_COUNTER = Counter()
REPEAT_SIGNATURES = Counter()
IP_PORT_ACTIVITY = defaultdict(set)
LIVE_MONITORING = True
USE_COLORS = True
ENABLE_TESTING = False
SESSION_ID = datetime.datetime.now().strftime("%H-%M-%S")
SESSION_START = datetime.datetime.now()

class Colors:
    RESET = "\033[0m" if USE_COLORS else ""
    INFO = "\033[94m" if USE_COLORS else ""
    LIVE = "\033[92m" if USE_COLORS else ""
    ERROR = "\033[91m" if USE_COLORS else ""

def setup_environment():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    day_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(script_dir, BASE_LOG_FOLDER, day_folder)
    report_dir = os.path.join(log_dir, "reports")
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    return log_dir, report_dir

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def extract_hour(timestamp):
    return timestamp.split()[1][:2]

def format_duration(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h:{m}m:{s}s"

def prompt_for_ports():
    global ENABLE_TESTING
    print("""
Choose port monitoring mode:
[1] Default ports (21, 22, 23, 80, 443)
[2] All ports (1-65535)
[3] Custom port (e.g. 8888)
[4] Default ports (TEST MODE)
""")
    choice = input("Your choice: ").strip()
    if choice == "1":
        return DEFAULT_PORTS
    elif choice == "2":
        return list(range(1, 65536))
    elif choice == "3":
        port = input("Enter port number: ").strip()
        if port.isdigit():
            return [int(port)]
        else:
            print("Invalid port, falling back to default.\n")
            return DEFAULT_PORTS
    elif choice == "4":
        ENABLE_TESTING = True
        return DEFAULT_PORTS
    else:
        print("Invalid choice, using default.\n")
        return DEFAULT_PORTS

def get_flags():
    global LIVE_MONITORING, USE_COLORS, ENABLE_TESTING
    args = sys.argv[1:]
    flags = [arg for arg in args if arg.startswith("--")]
    values = [arg for arg in args if not arg.startswith("--")]
    if "--no-color" in flags:
        USE_COLORS = False
    if "--no-live" in flags:
        LIVE_MONITORING = False
    if "--test" in flags:
        ENABLE_TESTING = True
    return values

def get_ports_from_arg(arg):
    if arg == "default":
        return DEFAULT_PORTS
    elif arg == "all":
        return list(range(1, 65536))
    elif arg.isdigit():
        return [int(arg)]
    else:
        print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Invalid argument '{arg}'. Falling back to default.\n")
        return DEFAULT_PORTS

def log_event(port, client_ip, data=None):
    filename = os.path.join(LOG_FOLDER, f"port_{port}.log")
    timestamp = get_timestamp()
    entry = f"[{timestamp}] Connection from {client_ip}"
    if data:
        entry += f" | Data: {data}"
    SESSION_LOG[port].append(entry)
    IP_COUNTER[client_ip] += 1
    HOUR_COUNTER[extract_hour(timestamp)] += 1
    IP_PORT_ACTIVITY[client_ip].add(port)
    if data:
        REPEAT_SIGNATURES[data.strip()] += 1

    with open(filename, "a") as f:
        f.write("\n" + f"--- Session {SESSION_ID} ---\n" if os.path.getsize(filename) == 0 else "")
        f.write(entry + "\n")

    if os.path.getsize(filename) > MAX_LOG_SIZE_MB * 1024 * 1024:
        os.rename(filename, filename + ".old")

    if LIVE_MONITORING:
        print(f"{Colors.LIVE}[LIVE]{Colors.RESET} {entry}\n")

def handle_connection(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(5)
    print(f"{Colors.INFO}[INFO]{Colors.RESET} Listening on port {port}\n")

    while True:
        client, addr = s.accept()
        client_ip = addr[0]
        log_event(port, client_ip)
        try:
            client.send(b"Welcome to secure service\n")
            data = client.recv(1024)
            if data:
                log_event(port, client_ip, data.decode(errors="ignore"))
        except Exception as e:
            log_event(port, client_ip, f"Error: {str(e)}")
            print(f"{Colors.ERROR}[ERROR]{Colors.RESET} {client_ip}: {e}\n")
        finally:
            client.close()

def simulate_test_traffic(ports):
    print(f"{Colors.INFO}[INFO]{Colors.RESET} Running test simulation on selected ports...\n")
    time.sleep(0.5)
    for port in ports:
        hits = random.randint(5, 20)
        for _ in range(hits):
            log_event(port, f"192.168.1.{random.randint(2, 254)}", "test-ping")
    print(f"{Colors.INFO}[INFO]{Colors.RESET} Test traffic simulation complete.\n")

def generate_session_report():
    _, report_dir = setup_environment()
    report_txt = os.path.join(report_dir, f"session_summary_{SESSION_ID}.txt")
    report_json = os.path.join(report_dir, f"session_summary_{SESSION_ID}.json")
    report_csv = os.path.join(report_dir, f"session_summary_{SESSION_ID}.csv")

    duration = (datetime.datetime.now() - SESSION_START).total_seconds()
    formatted_duration = format_duration(duration)

    with open(report_txt, "w") as report:
        report.write(f"Honeypot Session Report - {get_timestamp()}\n")
        report.write(f"Session started at: {SESSION_START.strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Session duration: {formatted_duration}\n")
        report.write("=" * 60 + "\n")

        report.write("\n[Port Activity]\n")
        for port in sorted(SESSION_LOG):
            report.write(f"\nPort {port} - {len(SESSION_LOG[port])} connections\n")
            report.write("-" * 40 + "\n")
            for entry in SESSION_LOG[port]:
                report.write(entry + "\n")

        report.write("\n[Top IP Addresses]\n")
        for ip, count in IP_COUNTER.most_common(10):
            report.write(f"{ip}: {count} connections\n")

        report.write("\n[Activity by Hour]\n")
        for hour, count in sorted(HOUR_COUNTER.items()):
            report.write(f"{hour}:00 - {count} connections\n")

        report.write("\n[Repeated Request Signatures]\n")
        for sig, count in REPEAT_SIGNATURES.most_common(10):
            if count > 1:
                report.write(f"'{sig}' - {count} times\n")

        report.write("\n[Potential Scanners]\n")
        for ip, ports in IP_PORT_ACTIVITY.items():
            if len(ports) > 2:
                report.write(f"{ip} scanned ports: {sorted(ports)}\n")
        report.write("\nEnd of Report\n")

    with open(report_json, "w") as f_json:
        json.dump({
            "start": SESSION_START.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": formatted_duration,
            "top_ips": IP_COUNTER.most_common(10),
            "activity_by_hour": dict(HOUR_COUNTER),
            "repeat_signatures": dict(REPEAT_SIGNATURES),
            "scanners": {ip: list(ports) for ip, ports in IP_PORT_ACTIVITY.items() if len(ports) > 2}
        }, f_json, indent=4)

    with open(report_csv, "w", newline='') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(["IP", "Total Connections", "Ports Accessed"])
        for ip in IP_COUNTER:
            writer.writerow([ip, IP_COUNTER[ip], ",".join(map(str, IP_PORT_ACTIVITY[ip]))])

    print(f"{Colors.INFO}[INFO]{Colors.RESET} Session reports saved to {report_dir}\n")

def start_honeypot():
    global LOG_FOLDER
    LOG_FOLDER, _ = setup_environment()

    args = get_flags()
    if args:
        ports = get_ports_from_arg(args[0])
    else:
        ports = prompt_for_ports()

    threads = []
    print(f"{Colors.INFO}[INFO]{Colors.RESET} Starting listeners...\n")
    for port in ports:
        t = threading.Thread(target=handle_connection, args=(port,), daemon=True)
        t.start()
        threads.append(t)

    if ENABLE_TESTING:
        time.sleep(0.5)
        simulate_test_traffic(ports)

    print(f"{Colors.INFO}[INFO]{Colors.RESET} Honeypot running. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.INFO}[INFO]{Colors.RESET} Honeypot stopped.\n")
        generate_session_report()

if __name__ == "__main__":
    start_honeypot()
