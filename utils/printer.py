from termcolor import colored

def info(msg):
    print(colored("[*] " + msg, "cyan"))

def good(msg):
    print(colored("[+] " + msg, "green"))

def bad(msg):
    print(colored("[-] " + msg, "red"))

def payload_tested(payload):
    print(colored("[PAYLOAD] ", "white") + payload)

def reflected(payload):
    print(colored("[REFLECTED] ", "red") + payload)
