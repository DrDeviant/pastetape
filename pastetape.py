#!/usr/bin/env python
import os
import argparse
import sqlite3

from modules.scraper import PastebinScraper
from modules.web import init_web
from modules.utilities import log

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Real-time Pastebin archive scraper that looks for specified keywords.")
    parser.add_argument('-m', '--mode', choices=['watch', 'once', 'none'], default='none',
                        help="Pastebin scraping mode: watch - scrape the archive periodically, once - scrape the archive once, none - do not scrape")
    parser.add_argument('-r', '--refresh-rate', type=int, default=30,
                        help="Wait time between archive refreshes (watch mode).")
    parser.add_argument('-t', '--tor', action='store_true',
                        help="Connect to Pastebin via TOR (must have TOR installed).")
    parser.add_argument('-i', '--web-interface', action='store_true',
                        help="Launch the web interface.")
    parser.add_argument('--db', default='pastetape.sqlite',
                        help="Path to database file.")
    parser.add_argument('--port', type=int, default=8080,
                        help="Port for the web interface.")
    parser.add_argument('--debug', action='store_true',
                        help="Turn on debug mode.")
    args = parser.parse_args()

    if not os.path.exists(args.db):
        conn = sqlite3.connect(args.db)
        conn.execute("CREATE TABLE pastes(id, date, syntax)")

    pm = PastebinScraper(
        refresh_rate=args.refresh_rate,
        tor=args.tor,
        database=args.db
    )

    if args.mode == "once":
        pm.get_new_pastes()

    if args.web_interface:
        log(f"Launching web interface on port: {args.port}")
        init_web(pm, args.port, args.db, args.debug)