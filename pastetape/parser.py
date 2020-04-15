from datetime import datetime

from bs4 import BeautifulSoup

class PastebinParser:
    @staticmethod
    def get_all_pastes_in_archive(html):
        """
        @param: html (str) - raw HTML scraped from Pastebin archive
        @return: pastes_list (list) - list containing dicts with details from every paste from supplied archive page
        """
        soup = BeautifulSoup(html, 'html.parser')
        pastes = soup.find('table', class_='maintable').find_all('tr')[1:]
        pastes_list = []

        for paste in pastes:
            cells = paste.find_all('td')
            paste_title  = cells[0].a.text
            paste_link   = cells[0].a.get('href')
            paste_date   = datetime.today().strftime('%d-%m-%Y')
            paste_syntax = cells[2].a.text
            pastes_list.append({
                'title': paste_title,
                'link': paste_link,
                'date': paste_date,
                'syntax': paste_syntax
            })

        return pastes_list

    @staticmethod
    def get_paste_content(html):
        """
        @param: html (str) - raw HTML scraped from Pastebin /raw
        @return: paste_content (str) - string with Paste content
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('pre').text