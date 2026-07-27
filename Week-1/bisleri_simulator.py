import socket
import threading
import random
import time
from datetime import datetime

# Bisleri production plants and their respective ports
BRANCHES = [
    ("bisleri-mumbai", 9001),
    ("bisleri-delhi", 9002),
    ("bisleri-chennai", 9003),
]

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Bisleri-specific log messages
MESSAGE_TEMPLATES = {
    "INFO": [
        "Water batch#{oid} purified and sealed",
        "Delivery truck dispatched to Zone-{oid}",
        "Inventory updated for 20L jars (ID:{oid})",
        "Distributor#{oid} accepted the shipment",
    ],
    "WARNING": [
        "TDS levels slightly fluctuating in batch#{oid}",
        "Delivery delayed for truck#{oid} due to traffic",
        "Low stock warning on 500ml bottles at warehouse#{oid}",
    ],
    "ERROR": [
        "RO filter pressure failure in plant#{oid}",
        "Payment timeout for distributor#{oid}",
        "Truck#{oid} breakdown reported on highway",
    ],
    "DEBUG": [
        "Calibrating pH sensors for batch#{oid}",
        "Retrying DB write for inventory sync#{oid}",
    ],
}

def build_log_line(branch_name):
    level = random.choice(LEVELS)
    oid = random.randint(1000, 9999)
    message = random.choice(MESSAGE_TEMPLATES[level]).format(oid=oid)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} | {level} | {branch_name} | {message}\n"

def handle_client(conn, branch_name):
    print(f"[{branch_name}] Harvester connected, streaming Bisleri data...")
    try:
        while True:
            line = build_log_line(branch_name)
            conn.sendall(line.encode("utf-8"))
            time.sleep(random.uniform(0.1, 0.5)) 

            # Occasionally send a corrupted log to test the regex
            if random.random() < 0.05:
                conn.sendall(b"CORRUPTED_SENSOR_DATA_NO_STRUCTURE\n")
    except (BrokenPipeError, ConnectionResetError):
        print(f"[{branch_name}] Harvester disconnected.")
    finally:
        conn.close()

def run_branch_server(branch_name, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("127.0.0.1", port))
    server_sock.listen(1)
    print(f"[{branch_name}] listening on port {port}...")

    while True:
        conn, addr = server_sock.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(conn, branch_name), daemon=True
        )
        client_thread.start()

if __name__ == "__main__":
    threads = []
    for name, port in BRANCHES:
        t = threading.Thread(target=run_branch_server, args=(name, port), daemon=True)
        t.start()
        threads.append(t)

    print("\nAll Bisleri plant servers are up. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Bisleri simulator.") 