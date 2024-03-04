#!/usr/bin/env python3
import argparse
import logging
import sys
from typing import Optional
# sys.path.append('jeffchess')

from analysis import Championship, debug_game, PersonalAnaysis
from util import Util


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse for my personal chess data.")
    parser.add_argument("-q", "--quiet", action='store_true', help="Set *NO* verbose logging i.e.: loglevel = logging.WARN")
    parser.add_argument("-v", "--verbose", action='store_true', help="Set *VERBOSE* logging i.e.: loglevel = logging.DEBUG")
    parser.add_argument("-dg", "--debug_game", help="Load game and verify if there is some errors")
    parser.add_argument("-a", "--my_games_analysis_full", required=False, help="Show my games with some opponent (or all for full history)")
    parser.add_argument("-c", "--championship_stats", required=False, help="Show stats from championship (all for general or choose an opponent)")
    parser.add_argument("-r", "--rating", required=False, help="Calculate rating for everyone.")
    parser.add_argument("-p", "--latest_performance", required=False, help="Get latest performance as in fide site.")
    parser.add_argument("-f", "--rating_fluctuation", required=False, help="Calc rating fluctuation.")
    parser.add_argument("-m", "--min_games", required=False, help="Calc min games for each opponent.")

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
        debug_game(args.debug_game)
    elif args.my_games_analysis_full:
        jeff: PersonalAnaysis = PersonalAnaysis()
        opponent: Optional[str] = None if args.my_games_analysis_full == "all" else args.my_games_analysis_full
        jeff.my_games(opponent=opponent)
    elif args.championship_stats:
        championship: Championship = Championship()
        player: Optional[str] = None if args.championship_stats == "all" else args.championship_stats
        championship.stats(player=player)
    elif args.rating:
        jeff: PersonalAnaysis = PersonalAnaysis()
        opponent: Optional[str] = None if args.rating == "all" else args.rating
        jeff.rating(choosen=opponent)
    elif args.latest_performance:
        jeff: PersonalAnaysis = PersonalAnaysis()
        # TODO get number of games
        # number_games: int = 70 if type(args.latest_performance) is int and args.latest_performance > 70 else int(args.latest_performance)
        opponent: Optional[str] = None if type(args.latest_performance) is int else args.latest_performance
        jeff.latest_games_perfomance(number_games=17, opponent=opponent)  # max 70 in FIDE's site
    elif args.rating_fluctuation:
        jeff: PersonalAnaysis = PersonalAnaysis()
        # TODO get number of games
        # number_games: int = 70 if type(args.latest_performance) is int and args.rating_fluctuation > 70 else int(args.rating_fluctuation)
        opponent: Optional[str] = None if type(args.rating_fluctuation) is int else args.rating_fluctuation
        jeff.rating_fluctuation(number_games=17, opponent=opponent)  # max 70 in FIDE's site
    elif args.min_games:
        jeff: PersonalAnaysis = PersonalAnaysis()
        jeff.define_min_valid_game_for_rating()
    else:
        logging.error(Util.error("Can't work!! Please, inform all parameters!!"))
        sys.exit("Failed execution. Please, see the log above.")

    sys.exit(0)
