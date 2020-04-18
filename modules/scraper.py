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
        self.session.cookies.update({'cf_clearance': '8cb67966b325ea9febc40f5e0e6dd1cbb85f12b9-1587039877-0-250'})
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'})
        if tor:
            self.session.proxies = {
                'http': 'socks5h://localhost:9050',
                'https': 'socks5h://localhost:9050'
            }

        self.refresh_rate = refresh_rate

    def get_new_pastes(self):
        r = self.session.get(self.ARCHIVE_URL)
        print(r.text)
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

    def check_if_keywords(self, id, keywords):
        r = self.session.get(self.RAW_URL + id)

        is_found = False
        found = PastebinParser.find_keyword_in_paste(r.text, keywords)
        if found:
            log(f"Found '{found}' in paste with Pastebin ID: {id}")
            is_found = True

        return is_found


    def check_if_unavailable(self, id):
        r = self.session.get(self.RAW_URL + id)

        if r.status_code == 404:
            log(f"Found unavailable paste with Pastebin ID: {id}")
            return True
        else:
            return False
        
