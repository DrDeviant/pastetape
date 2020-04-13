import threading

import requests

from pastetape.parser import PastebinParser

class PastebinMonitor:
    ARCHIVE_URL = 'https://pastebin.com/archive'

    def __init__(self, watch: bool = True, tor: bool = False, refresh_rate: int = 30):
        self.session = requests.session()
        if tor:
            self.session.proxies = {
                'http': 'socks5h://localhost:9050',
                'https': 'socks5h://localhost:9050'
            }

        self.watch = watch
        self.refresh_rate = 30

    def refresh_archive(self):
        r = self.session.get(self.ARCHIVE_URL)
        pastes = PastebinParser.get_all_pastes_in_archive(r.text)
        print(pastes)