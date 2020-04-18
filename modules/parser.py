from datetime import datetime

from bs4 import BeautifulSoup

from modules.utilities import log

class PastebinParser:
    @staticmethod
    def get_all_pastes_in_archive(html):
        """
        @param: html (str) - raw HTML scraped from Pastebin archive
        @return: list containing dicts with details from every paste from supplied archive page
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            pastes = soup.find('table', class_='maintable').find_all('tr')[1:]
            pastes_list = []

            for paste in pastes:
                cells = paste.find_all('td')
                paste_id     = cells[0].a.get('href')[1:]
                paste_date   = datetime.today().strftime('%d-%m-%Y')
                paste_syntax = cells[2].a.text
                pastes_list.append({
                    'id': paste_id,
                    'date': paste_date,
                    'syntax': paste_syntax
                })

            return pastes_list
        except AttributeError:
            log("An error occurred while trying to scrape Pastebin!")
            return []

    @staticmethod
    def find_keyword_in_paste(html, keywords):
        """
        @param: html (str) - raw HTML scraped from Pastebin archive
        @param: keyword (list of str) - words to search for in paste
        @return: first keyword (str) which was found in paste or None
        """
        for keyword in keywords:
            if keyword in html:
                return keyword

        return None