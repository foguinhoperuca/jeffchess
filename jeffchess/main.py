#!/usr/bin/env python3
import argparse
import logging
import sys
from typing import Optional
sys.path.append('jeffchess')

from termcolor import colored

import analysis
from analysis import Championship, PersonalAnaysis
from util import Util


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse for my personal chess data.")
    parser.add_argument("-q", "--quiet", action='store_true', help="Set *NO* verbose logging i.e.: loglevel = logging.WARN")
    parser.add_argument("-v", "--verbose", action='store_true', help="Set *VERBOSE* logging i.e.: loglevel = logging.DEBUG")
    parser.add_argument("-dg", "--debug_game", help="Load game and verify if there is some errors")
    parser.add_argument("-f", "--my_games_analysis_full", required=False, help="Show my games with some opponent (or all for full history)")
    parser.add_argument("-c", "--championship_stats", required=False, help="Show stats from championship (all for general or choose an opponent)")
    parser.add_argument("-r", "--rating", required=False, help="Calculate rating for everyone.")

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

    logging.basicConfig(level=loglevel, format=logformat)

    if args.verbose:
        logging.debug(Util.debug("args: {v}".format(v=vars(args))))

    # TODO implement validation of game result (José roberto Oliveira vs Emerson Sbrana) was 2x
    stats = None
    if args.debug_game:
        analysis.debug_game(args.debug_game)
    elif args.my_games_analysis_full:
        jeff = PersonalAnaysis()
        opponent: Optional[str] = None if args.my_games_analysis_full == 'all' else args.my_games_analysis_full
        jeff.my_games(opponent=opponent)
    elif args.championship_stats:
        championship = Championship()
        player: Optional[str] = None if args.championship_stats == 'all' else args.championship_stats
        championship.stats(player=player)
    elif args.rating:
        jeff = PersonalAnaysis()
        jeff.rating(opponent=args.rating)
    else:
        logging.error(Util.error("Can't work!! Please, inform all parameters!!"))
        sys.exit("Failed execution. Please, see the log above.")

    sys.exit(0)
