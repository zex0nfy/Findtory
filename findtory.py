#!/usr/bin/env python3
import requests
import argparse
import threading
import queue
import urllib.parse
from datetime import datetime
from colorama import init as colorama_init, Fore, Style
from tqdm import tqdm

BANNER = r"""
  ______ _           _   _              
 |  ____| |         | | (_)             
 | |__  | | ___  ___| |_ _  ___  _ __   
 |  __| | |/ _ \/ __| __| |/ _ \| '_ \  
 | |    | |  __/\__ \ |_| | (_) | | | | 
 |_|    |_|\___||___/\__|_|\___/|_| |_| 
                                         
Findtory - Finds any directory from a website
"""

def color_print(text, color):
    print(color + Style.BRIGHT + text + Style.NORMAL + Fore.RESET)

class DirBruteForcer:
    def __init__(self, base_url, wordlist, extensions=None, threads=10,
                 status_codes=None, timeout=5, output_file=None):
        self.base_url = base_url.rstrip('/')
        self.wordlist = wordlist
        self.extensions = extensions or []
        self.threads = threads
        self.timeout = timeout
        self.output_file = output_file
        self.status_codes = set(status_codes) if status_codes else {200, 301, 302, 403}
        self.q = queue.Queue()
        self.lock = threading.Lock()
        self.discovered = []
        self.total_tasks = 0
        self.progress = None

    def load_words(self):
        total = 0
        with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if word:
                    self.q.put(word)
                    total += 1
                    for ext in self.extensions:
                        self.q.put(f"{word}.{ext}")
                        total += 1
        self.total_tasks = total
        return total

    def worker(self):
        while not self.q.empty():
            path = self.q.get()
            url = urllib.parse.urljoin(self.base_url + '/', path)
            try:
                resp = requests.get(url, timeout=self.timeout, allow_redirects=False)
                code = resp.status_code
                if code in self.status_codes:
                    color = (
                        Fore.GREEN if code == 200 else
                        Fore.BLUE if code in (301, 302) else
                        Fore.YELLOW if code == 403 else
                        Fore.RED
                    )
                    result = f"[{code}] {url}"
                    with self.lock:
                        color_print(result, color)
                        self.discovered.append(result)
                        if self.output_file:
                            with open(self.output_file, 'a', encoding='utf-8') as out_f:
                                out_f.write(result + '\n')
            except requests.RequestException:
                pass
            finally:
                with self.lock:
                    if self.progress:
                        self.progress.update(1)
                self.q.task_done()

    def run(self):
        colorama_init()
        print(BANNER)
        print(f"Starting scan at {datetime.now().isoformat()} on {self.base_url}")
        total = self.load_words()
        print(f"Loaded {total} paths using {self.threads} threads")
        if self.output_file:
            open(self.output_file, 'w').close()
        self.progress = tqdm(total=self.total_tasks, desc="Progress", unit="req")
        threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.threads)]
        for t in threads:
            t.start()
        self.q.join()
        self.progress.close()
        print(f"\nScan completed at {datetime.now().isoformat()}")
        print(f"Discovered {len(self.discovered)} paths")


def parse_args():
    parser = argparse.ArgumentParser(description="Findtory - Finds any directory from a website")
    parser.add_argument('url', help='Base URL (e.g., https://example.com)')
    parser.add_argument('-w', '--wordlist', required=True, help='Path to wordlist file')
    parser.add_argument('-e', '--extensions', default='', help='Comma-separated extensions')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')
    parser.add_argument('-c', '--codes', help='Comma-separated status codes (default:200,301,302,403)')
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('--timeout', type=int, default=5, help='Request timeout in seconds')
    return parser.parse_args()


def main():
    args = parse_args()
    exts = [e.strip() for e in args.extensions.split(',') if e.strip()]
    codes = [int(c) for c in args.codes.split(',')] if args.codes else None
    brute = DirBruteForcer(
        args.url, args.wordlist, extensions=exts,
        threads=args.threads, status_codes=codes,
        timeout=args.timeout, output_file=args.output
    )
    brute.run()

if __name__ == '__main__':
    main()
