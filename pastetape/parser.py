from datetime import datetime
from time import time

from bs4 import BeautifulSoup

class PastebinParser:
    @staticmethod
    def get_all_pastes_in_archive(html):
        soup = BeautifulSoup(html, 'html.parser')
        pastes = soup.find('table', class_='maintable').find_all('tr')[1:]
        pastes_dict = {'pastes': []}

        for paste in pastes:
            cells = paste.find_all('td')
            paste_title  = cells[0].a.text
            paste_link   = cells[0].a.get('href')
            paste_time   = PastebinParser.format_archive_datetime(cells[1].text)
            paste_syntax = cells[2].a.text
            pastes_dict['pastes'].append({
                'title': paste_title,
                'link': paste_link,
                'datetime': paste_time,
                'syntax': paste_syntax
            })

        return pastes_dict

    @staticmethod
    def get_paste_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        pass

    @staticmethod
    def format_archive_datetime(posted_time):
        if 'sec' in posted_time:
            timestamp = time() - int(posted_time.split()[0])
        elif 'min' in posted_time:
            timestamp = time() - int(posted_time.split()[0]) * 60
        else:
            return "Unknown datetime"

        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')