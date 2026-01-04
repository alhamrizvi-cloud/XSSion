#!/usr/bin/env python3

import sys
import requests
import urllib.parse
import time
from termcolor import colored

requests.packages.urllib3.disable_warnings()

# ---------------- ASCII BANNER ----------------
def banner():
    print(colored(r"""
 ___ ___ _______ _______ __              
|   |   |     __|     __|__|.-----.-----.
|-     -|__     |__     |  ||  _  |     |
|___|___|_______|_______|__||_____|__|__|
                                         
        XSSion – Reflected XSS Scanner
        [ Made by: @alhamrizvii ]
""", "cyan"))

# ---------------- ARG CHECK ----------------
if len(sys.argv) != 3:
    print("Usage: python3 xssion.py <URL> <payloads.txt>")
    sys.exit(1)

url = sys.argv[1]
payload_file = sys.argv[2]

THREADS = 1          # kept for info (single-thread for clarity)
TIMEOUT = 10         # request timeout in seconds

# ---------------- LOAD PAYLOADS ----------------
with open(payload_file, "r", errors="ignore") as f:
    payloads = [x.strip() for x in f if x.strip()]

parsed = urllib.parse.urlparse(url)

# IMPORTANT FIX
params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

if not params:
    print(colored("[!] No parameters found in URL", "red"))
    sys.exit(1)

# ---------------- INFO ----------------
banner()
print(colored("[+] Target URL :", "green"), url)
print(colored("[+] Parameters :", "green"), ", ".join(params.keys()))
print(colored("[+] Payloads   :", "green"), len(payloads))
print(colored("[+] Threads    :", "green"), THREADS)
print(colored("[+] Timeout    :", "green"), f"{TIMEOUT}s")
print(colored("[+] Output     :", "green"), "XSSion.txt")
print(colored("-" * 60, "cyan"))

# ---------------- SCAN ----------------
start_time = time.time()

for param in params:
    for payload in payloads:
        test_params = params.copy()
        test_params[param] = payload

        new_query = urllib.parse.urlencode(test_params, doseq=True)
        test_url = parsed._replace(query=new_query).geturl()

        print(colored(f"[TESTING] param={param} payload={payload}", "yellow"))

        try:
            r = requests.get(test_url, timeout=TIMEOUT, verify=False)

            if payload in r.text:
                print(colored(f"[REFLECTED] {test_url}\n", "red"))
                with open("XSSion.txt", "a") as out:
                    out.write(f"[XSS] {test_url} | {payload}\n")
            else:
                print(colored("[NOT REFLECTED]\n", "white"))

        except Exception as e:
            print(colored(f"[ERROR] {e}\n", "magenta"))

end_time = time.time()

print(colored("-" * 60, "cyan"))
print(colored("[✓] Scan completed", "green"))
print(colored("[✓] Time taken :", "green"), f"{round(end_time - start_time, 2)} seconds")
