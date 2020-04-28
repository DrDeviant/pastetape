#!/usr/bin/env python
import os
import argparse
import sqlite3

from modules.scraper import PastebinScraper
from modules.web import init_web
from modules.utilities import log

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pastebin archive scraper with web interface for searching through pastes.")
    parser.add_argument('-s', '--scrape', action='store_true',
                        help="Scrape the Pastebin archive for new pastes.")
    parser.add_argument('-t', '--tor', action='store_true',
                        help="Connect to Pastebin via TOR (must have TOR installed).")
    parser.add_argument('--cf-clearance', default="",
                        help="Cloudflare Clearance cookie for Pastebin - supply when blocked by CF.")
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
        conn.execute("CREATE TABLE pastes(id, content, date, syntax)")

    pm = PastebinScraper(
        tor=args.tor,
        database=args.db,
        cf_clearance=args.cf_clearance
    )

    if args.scrape:
        pm.get_new_pastes()

    if args.web_interface:
        log(f"Launching web interface on port: {args.port}")
        init_web(pm, args.port, args.db, args.debug)