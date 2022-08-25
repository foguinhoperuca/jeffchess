#!/usr/bin/env python3
import sys
sys.path.append('jeffchess')
from termcolor import colored
import configparser
from decimal import Decimal
import logging
import argparse
from util import Util
import game_analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Parse for my personal chess data.")
    parser.add_argument("-q", "--quiet", action = 'store_true', help = "Set *NO* verbose logging i.e.: loglevel = logging.WARN")
    parser.add_argument("-v", "--verbose", action = 'store_true', help = "Set *VERBOSE* logging i.e.: loglevel = logging.DEBUG")
    parser.add_argument("-dg", "--debug_game", help = "Load game and verify if there is some errors")
    parser.add_argument("-s", "--stats", required = False, help = "Calc stats")

    args = parser.parse_args()
    if args.verbose:
        loglevel = logging.DEBUG
        logformat = Util.LOG_FORMAT_DEBUG
    elif args.quiet:
        loglevel = logging.WARN
        # TODO log to file in this case
        logformat = Util.LOG_FORMAT_SIMPLE
    else:
        loglevel = logging.INFO
        logformat = Util.LOG_FORMAT_FULL

    logging.basicConfig(level = loglevel, format = logformat)

    if args.verbose:
        logging.debug(Util.debug("args: {v}".format(v = vars(args))))

    stats = None
    if args.debug_game:
        game_analysis.debug_game(args.debug_game)
    elif args.stats == "padoca-2022-02":
        game_analysis.padoca_championship_2022_02()
    elif args.stats == "jeff":
        game_analysis.my_games()
    else:
        logging.error(Util.error("Can't work!! Please, inform all parameters!!"))
        sys.exit("Failed execution. Please, see the log above.")

    sys.exit(0)
