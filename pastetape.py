#!/usr/bin/env python
import os
import argparse
import sqlite3

from modules.scraper import PastebinScraper
from modules.web import init_web

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Real-time Pastebin archive scraper that looks for specified keywords.")
    parser.add_argument('-w', '--watch', action='store_true',
                        help="Watch the Pastebin archive for new pastes.")
    parser.add_argument('-r', '--refresh-rate', type=int, default=30,
                        help="Wait time between archive refreshes (watch mode).")
    parser.add_argument('-t', '--tor', action='store_true',
                        help="Connect to Pastebin via TOR (must have TOR installed).")
    parser.add_argument('-d', '--db', default='pastetape.sqlite',
                        help="Path to database file.")
    parser.add_argument('-i', '--web-interface', action='store_true',
                        help="Launch the web interface.")
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help="Port for the web interface.")
    args = parser.parse_args()

    if not os.path.exists(args.db):
        conn = sqlite3.connect(args.db)
        conn.execute("CREATE TABLE pastes(id, date, syntax)")

    pm = PastebinScraper(
        watch=args.watch,
        refresh_rate=args.refresh_rate,
        tor=args.tor,
        database=args.db
    )

    pm.get_new_pastes()

    if args.web_interface:
        print("[!] Launching web interface...")
        init_web(pm, args.port, args.db)