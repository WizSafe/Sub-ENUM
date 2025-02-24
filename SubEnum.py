import os
import time
import requests
import concurrent.futures
from termcolor import colored

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(colored("""
 ▗▄▄▖█  ▐▌▗▖   ▗▄▄▄▖▄▄▄▄  █  ▐▌▄▄▄▄  
▐▌   ▀▄▄▞▘▐▌   ▐▌   █   █ ▀▄▄▞▘█ █ █ 
 ▝▀▚▖     ▐▛▀▚▖▐▛▀▀▘█   █      █   █ 
▗▄▄▞▘     ▐▙▄▞▘▐▙▄▄▖                 
                                     
Developed By WizSafe Technologies""", "red", attrs=["bold"]))

def loading_animation():
    animation = ["|", "/", "-", "\\"]
    for _ in range(10):
        for symbol in animation:
            print(f"\r{colored('Scanning...', 'yellow', attrs=['bold'])} {symbol}", end="", flush=True)
            time.sleep(0.1)
    print("\n")

def check_subdomain(sub, domain):
    for protocol in ["http", "https"]:
        url = f"{protocol}://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(colored(f"[+] Found: {url}", "green", attrs=["bold"]))
                return url
        except requests.ConnectionError:
            pass
    return None

def enumerate_subdomains(domain, wordlist):
    found_subdomains = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_subdomain, sub, domain) for sub in wordlist]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found_subdomains.append(result)
    return found_subdomains

def main():
    clear_screen()
    banner()
    domain = input(colored("\nEnter the target domain: ", "cyan", attrs=["bold"]))
    
    # Large wordlist
    wordlist = ["www", "mail", "ftp", "blog", "admin", "api", "test", "dev", "shop", "dashboard", "webmail", "secure", "portal", "staging", "vpn", "beta", "cloud", "cdn", "pay", "login", "accounts", "db", "hr", "office", "docs"]
    
    print(colored("\nStarting Subdomain Enumeration...", "yellow", attrs=["bold"]))
    loading_animation()
    subdomains = enumerate_subdomains(domain, wordlist)
    
    if not subdomains:
        print(colored("\nNo subdomains found.", "red", attrs=["bold"]))
    else:
        print(colored("\nSubdomain enumeration completed!", "blue", attrs=["bold"]))
        with open("found_subdomains.txt", "w") as f:
            for sub in subdomains:
                f.write(sub + "\n")
        print(colored("\nResults saved in found_subdomains.txt", "green", attrs=["bold"]))

if __name__ == "__main__":
    main()
