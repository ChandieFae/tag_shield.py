import requests
from bs4 import BeautifulSoup

class TagShield:
    TRACKER_SIGNATURES = [
        'googletagmanager.com',
        'google-analytics.com',
        'facebook.net',
        'ads.twitter.com',
        'snapchat.com',
        'tiktok.com',
        'clarity.ms',
        'linkedin.com',
        'hotjar.com',
        'crazyegg.com',
        'doubleclick.net',
        'adroll.com'
    ]

    ALLOW_LIST = [
        'google-analytics.com',
        'googletagmanager.com'
    ]

    def __init__(self):
        self.results = {}

    def scan_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            trackers = []

            for script in scripts:
                src = script.get('src', '') or ''
                if src.startswith('http'):
                    status = self.get_tracker_status(src)
                    trackers.append((src, status))

            self.results[url] = trackers
        except Exception as e:
            self.results[url] = [("ERROR", str(e))]

    def get_tracker_status(self, src):
        for sig in self.TRACKER_SIGNATURES:
            if sig in src:
                return "FLAGGED" if sig not in self.ALLOW_LIST else "ALLOWED"
        return "UNLISTED"

    def report(self):
        print("\n🛡️ TAG SHIELD REPORT")
        for url, trackers in self.results.items():
            print(f"\n🔍 {url}")
            for src, status in trackers:
                print(f"  [{status}] {src}")

if __name__ == "__main__":
    shield = TagShield()
    urls = [
        "https://www.tcappliancehvac.com",
        "https://www.tcappliancerepairman.com"
    ]
    for url in urls:
        shield.scan_page(url)
    shield.report()
