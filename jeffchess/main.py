#!/usr/bin/env python3
import sys
sys.path.append('jeffchess')
from termcolor import colored
import configparser
# import datetime
from decimal import Decimal
# import xml.etree.ElementTree as ET
# from abc import abstractmethod
import logging
import argparse
import sys
from pprint import pprint
from util import Util
import games

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Parse for my personal chess data.")
    parser.add_argument("-q", "--quiet", action = 'store_true', help = "Set *NO* verbose logging i.e.: loglevel = logging.WARN")
    parser.add_argument("-v", "--verbose", action = 'store_true', help = "Set *VERBOSE* logging i.e.: loglevel = logging.DEBUG")
    parser.add_argument("-s", "--stats", required = False, help = "Calc stats")
    parser.add_argument("-m", "--manual", help = "Manual load game")

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
    if args.manual:
        print(args.manual)
        games.manual_load(args.manual)
    elif args.stats == "all":
        stats = games.padoca_championship_2022_02()
        pprint(stats)
    elif args.stats == "jeff":
        stats = games.my_games()
    elif args.stats == "TODO regex timestamp":
        stats = "TODO parse a game"
    else:
        try:
            stats = "TODO parse stats.csv"
        except Exception as error:
            logging.error(Util.error("Can't work!! Please, inform all parameters!!"))
            logging.error(Util.error("message: {m}".format(m = error)))
            logging.error(Util.error("type: {t} with args {args}".format(t = type(error), args = error.args)))
            sys.exit("Failed execution. Please, see the log above.")

    logging.debug(Util.debug(vars(games)))

    # if account is None:
    #     logging.error(Util.error("Failed with account: need be defined!!!"))
    #     sys.exit("Failed execution. Please, see the log above.")

    # TODO calc stats
    sys.exit(0)
