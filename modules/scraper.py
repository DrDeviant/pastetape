import sqlite3

import requests

from modules.parser import PastebinParser
from modules.utilities import log

class PastebinScraper:
    RAW_URL = 'https://pastebin.com/raw/'
    ARCHIVE_URL = 'https://pastebin.com/archive'

    def __init__(self, tor: bool = False, refresh_rate: int = 30, database: str = 'pastetape.sqlite'):
        self.db_conn = sqlite3.connect(database)
        self.db_cur = self.db_conn.cursor()

        self.session = requests.session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'})
        if tor:
            self.session.proxies = {
                'http': 'socks5h://localhost:9050',
                'https': 'socks5h://localhost:9050'
            }

        self.refresh_rate = refresh_rate

    def get_new_pastes(self):
        r = self.session.get(self.ARCHIVE_URL)
        pastes = PastebinParser.get_all_pastes_in_archive(r.text)

        for paste in pastes:
            self.db_cur.execute("SELECT 1 FROM pastes WHERE id = ?", [paste['id']])
            
            if not self.db_cur.fetchone():
                log(f"New paste fetched with Pastebin ID: {paste['id']}")
                self.db_cur.execute("INSERT INTO pastes VALUES (?, ?, ?)",
                                    (paste['id'], paste['date'], paste['syntax']))

        self.db_conn.commit()

    def get_raw_paste(self, id):
        r = self.session.get(self.RAW_URL + id)
        
        return r.text

    def check_if_unavailable(self, id):
        r = self.session.get(self.RAW_URL + id)

        if r.status_code == 404:
            log(f"Found unavailable paste with Pastebin ID: {id}")
            return True
        else:
            return False
        