#!/usr/bin/env python3
import sys
sys.path.append('jeffchess')
from termcolor import colored
import configparser
from decimal import Decimal
import logging
import argparse
from util import Util
import analysis

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

    # TODO implement validation of game result (José roberto Oliveira vs Emerson Sbrana) was 2x
    stats = None
    if args.debug_game:
        analysis.debug_game(args.debug_game)
    elif args.stats == "padoca-2022-02":
        analysis.padoca_championship("stats.csv")
    elif args.stats == "padoca-cup-2022":
        analysis.padoca_championship(championship_data_file="padoca_cup_2022.csv", set_unfinished_column=False)
    elif args.stats == "jeff":
        analysis.my_games()

    elif args.stats == "games_by_player":
        analysis.games_by_player("Jefferson Campos")

    else:
        logging.error(Util.error("Can't work!! Please, inform all parameters!!"))
        sys.exit("Failed execution. Please, see the log above.")

    sys.exit(0)
