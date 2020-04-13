#!/usr/bin/env python

import argparse

from pastetape.monitor import PastebinMonitor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Real-time Pastebin archive monitor that looks for specified keywords.")
    parser.add_argument('-w', '--watch', action='store_true',
                        help="Watch the Pastebin archive for new pastes.")
    parser.add_argument('-r', '--refresh-rate', type=int, default=30,
                        help="Wait time between archive refreshes (watch mode).")
    parser.add_argument('-t', '--tor', action='store_true',
                        help="Connect to Pastebin via TOR (must have TOR installed).")
    args = parser.parse_args()

    pm = PastebinMonitor(
        watch=args.watch,
        refresh_rate=args.refresh_rate,
        tor=args.tor
    )
    pm.refresh_archive()