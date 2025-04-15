import threading
import time
import requests
from termcolor import cprint, colored
from playwright.sync_api import sync_playwright
import warnings
import sys

warnings.filterwarnings("ignore", category=DeprecationWarning)

# WAF Detection
def detect_waf(url):
    try:
        headers = {
            "User-Agent": "XSS-Scanner/1.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        print("\n[+] WAF Headers:")
        for key in ["Server", "X-Powered-By", "CF-Ray", "X-Akamai-Transformed", "X-Sucuri-ID", "X-Content-Type-Options", "Strict-Transport-Security"]:
            if key in response.headers:
                print(f"    {key}: {response.headers[key]}")
        if response.status_code != 200:
            print(f"[-] HTTP Response Code: {response.status_code}")
    except Exception as e:
        print("[-] WAF detection failed:", str(e))

# Worker thread
def scan_xss(base_url, payloads, thread_id, headless):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        alert_triggered = False

        def handle_dialog(dialog):
            nonlocal alert_triggered
            if not alert_triggered:
                alert_triggered = True
                try:
                    dialog_type = dialog.type
                    cprint(f"[!] {dialog_type.upper()} detected: {dialog.message}", "green")
                    dialog.accept()
                except Exception as e:
                    if "already handled" in str(e):
                        cprint("[!] Dialog already handled, skipping accept().", "yellow")
                    else:
                        cprint(f"[!] Unexpected dialog error: {e}", "yellow")

        page.on("dialog", handle_dialog)

        for payload in payloads:
            full_url = f"{base_url}{payload}"
            cprint(f"[Thread {thread_id}] Testing payload: {payload}", "cyan")
            alert_triggered = False

            try:
                page.goto(full_url, timeout=10000)
                time.sleep(2)

                if alert_triggered:
                    cprint(f"[+] ALERT Detected! Payload: {payload}", "green")
                    cprint(f"[+] URL: {full_url}", "green")
                else:
                    cprint(f"[-] No alert for: {payload}", "red")

            except Exception as e:
                cprint(f"[!] Error with payload {payload}: {e}", "yellow")

        context.close()
        browser.close()

# Main
def main():
    try:
        with open("url.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        cprint("[!] url.txt file not found!", "red")
        sys.exit()

    if not urls:
        cprint("[!] No URLs found in url.txt", "red")
        sys.exit()

    thread_count = int(input("Number of threads: ").strip())
    headless_choice = input("Run in headless mode? (y/n): ").lower()
    headless = headless_choice == 'y'

    try:
        with open("payloads.txt", "r") as f:
            payloads = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        cprint("[!] payloads.txt file not found!", "red")
        sys.exit()

    if not payloads:
        cprint("[!] No payloads found in payloads.txt", "red")
        sys.exit()

    for base_url in urls:
        detect_waf(base_url)

        chunk_size = len(payloads) // thread_count + 1
        threads = []

        print(f"\n[+] Starting XSS Scan for {base_url}...\n")

        for i in range(thread_count):
            chunk = payloads[i*chunk_size:(i+1)*chunk_size]
            t = threading.Thread(target=scan_xss, args=(base_url, chunk, i+1, headless))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    print("\n[+] Scan Complete ✅")

if __name__ == "__main__":
    main()
