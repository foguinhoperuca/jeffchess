import chess.pgn
import os
import csv
import logging
from collections import OrderedDict
from pprint import pprint
from prettytable import PrettyTable
from util import Util

def padoca_championship_2022_02():
    # stats.csv --> timestamp;white;black;result;observation
    with open("data/stats.csv") as stats:
        csv_reader = csv.reader(stats, delimiter = ';')
        total_games = 0
        classification = {
            "Emerson Sbrana": {
                "points": 0,
                "unfinished": 0
            },
            "Jefferson Campos": {
                "points": 0,
                "unfinished": 0
            },
            "Jefferson Nunes": {
                "points": 0,
                "unfinished": 0
            },
            "João Carlos Oliveira": {
                "points": 0,
                "unfinished": 0
            },
            "José Carlos Bento Dias da Rocha": {
                "points": 0,
                "unfinished": 0
            },
            "José Roberto Oliveira": {
                "points": 0,
                "unfinished": 0
            },
            "Mário Sérgio Bueno Miranda": {
                "points": 0,
                "unfinished": 0
            },
        }
        for row in csv_reader:
            if total_games == 0:
                total_games = 1
                continue

            total_games += 1
            match row[3]:
                case "1-0":
                    logging.debug("white wins! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[1]]["points"] += 1
                case "0-1":
                    logging.debug("black wins! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[2]]["points"] += 1
                case "0,5-0,5":
                    logging.debug("draw! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[1]]["points"] += 0.5
                    classification[row[2]]["points"] += 0.5
                case "*":
                    logging.debug("unfinished! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[1]]["unfinished"] += 1
                    classification[row[2]]["unfinished"] += 1
                case _:
                    logging.debug("got an invalid value! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))

        logging.info(Util.info("total games: {t}".format(t = total_games)))

        od = OrderedDict(sorted(classification.items(), key = lambda x: x[1]["points"], reverse = True))
        ptable = PrettyTable()
        ptable.field_names = ['Player', 'Points', 'Unfinished']
        
        for key, value in od.items():
            points, unfinished = value.items()
            ptable.add_row([key, points[1], unfinished[1]])

        logging.debug(Util.debug("args: {v}".format(v = od)))
        print(ptable)

# w 79 }
# d 15 }
# l 74 }
# u 43 }
# a 3 }

# manual my stats:
# white:
# win: 44
# draw: 10
# lose: 24
# abandoned: 1
# unfinished: 16
# -------
# total: 49 points
# ******************************
# black:
# win: 35
# draw: 5
# lose: 23
# abandoned: 2
# unfinished: 27
# --------
# total: 37.5
# pontuação: 86.5
def my_games():
    # TODO implement  more detailed analisys
    # championship.ods #	Player	White	Black	Total	Unfinished	JUN/2022	JUL/2022	AUG/2022
    total_errors = 0
    total_games = 0
    total_win_loss = 0
    total_draws = 0
    unfinished = 0

    leader_board = {
        "player": {
            "white": {
                "win": 0,
                "lost": 0,
                "draw": 0,
                "unfinished": 0
            },
            "black": {
                "win": 0,
                "lose": 0,
                "draw": 0,
                "unfinished": 0
            }
        }
    }
    unknow_games = 0

    with open("data/jeff_stats.csv", "w") as s:
        writer = csv.writer(s, delimiter = ";")
        writer.writerow(["timestamp", "white", "black", "result"])
        for path in os.listdir("data/pgn/mgr/"):
            with open("data/pgn/mgr/" + path, encoding = "utf-8") as pgn:
                total_games += 1
                game = chess.pgn.read_game(pgn)
                if len(game.errors) != 0:
                    print(Util.error("file: {f}".format(f = path)))
                    total_errors += 1

                writer.writerow([game.headers["Date"], game.headers["White"], game.headers["Black"], game.headers["Result"]])
                # print("--------------------------------------------") }
                if game.headers["Result"] == "1-0" or game.headers["Result"] == "0-1":
                    total_win_loss += 1
                elif game.headers["Result"] == "1/2-1/2":
                    total_draws += 1
                elif game.headers["Result"] == "*":
                    # print("file: {f!#\ white: {w!#\ black: {b!#\ result: {r!#\".format(f = path, w = game.headers["White"], b = game.headers["Black"], r = game.headers["Result"])) }
                    unfinished += 1

                
                if game.headers["White"] == "Jefferson Campos":
                    if game.headers["Result"] == "1-0":
                        leader_board["player"]["white"]["win"] += 1
                    elif game.headers["Result"] == "0-1":
                        leader_board["player"]["white"]["lose"] += 1
                    elif game.headers["Result"] == "1/2-1/2":
                        leader_board["player"]["white"]["draw"] += 1
                    elif game.headers["Result"] == "*":
                        leader_board["player"]["white"]["unfinished"] += 1
                    else:
                        raise Exception("Unexpected Game Result")
                elif game.headers["Black"] == "Jefferson Campos":
                    if game.headers["Result"] == "1-0":
                        leader_board["player"]["black"]["lose"] += 1
                    elif game.headers["Result"] == "0-1":
                        leader_board["player"]["black"]["win"] += 1
                    elif game.headers["Result"] == "1/2-1/2":
                        leader_board["player"]["black"]["draw"] += 1
                    elif game.headers["Result"] == "*":
                        leader_board["player"]["black"]["unfinished"] += 1
                    else:
                        raise Exception("Unexpected Game Result")
                elif game.headers["White"] == "?" and game.headers["Black"] == "?":
                    unknow_games += 1
                else:
                    FIXME 
                    raise Exception("Unexpected Player: neither black/white is Jefferson Campos")

    ptable = PrettyTable()
    ptable.field_names = ['TOTAL GAMES', 'WIN/LOSS', 'DRAWS', 'UNFINISHED', 'ERRORS']
    ptable.add_row([total_games, total_win_loss, total_draws, unfinished, total_errors])
    print(ptable)
    logging.info(Util.info("total_games: {g} - total_win_loss: {f} - total unfinished: {u} - total_draw:{d} - total_errors: {e}".format(u = unfinished, e = total_errors, g = total_games, f = total_win_loss, d = total_draws)))

def debug_game(game):
    logging.debug(Util.debug("Game was: {g}".format(g = game)))
    with open("data/pgn/mgr/{g}.pgn".format(g = game), encoding = "utf-8") as pgn:
        game = chess.pgn.read_game(pgn)
        print(len(game.errors), game.errors)
        print(game)


# TODO fix files using sed: sed -i -e 's/Hefferson Campos/Jefferson Campos/g' jeff_stats.csv

# White: }
# w: Jefferson Campos 08 - 00 João Carlos }
# l: Jefferson Campos 00 - 11 João Carlos }
# d: Jefferson Campos 04 - 04 João Carlos }
# *: Jefferson Campos 06 - 06 João Carlos }

# Black: }
# w: João Carlos 10 - 00 Jefferson Campos }
# l: João Carlos 00 - 13 Jefferson Campos }
# d: João Carlos 02 - 02 Jefferson Campos }
# *: João Carlos 15 - 15 Jefferson Campos }

# jeff 21 - 21 joao carlos }

# ---- }

# White: }
# w: Jefferson Campos 16 - 00 José Roberto }
# l: Jefferson Campos 00 - 06 José Roberto }
# d: Jefferson Campos 01 - 01 José Roberto }
# *: Jefferson Campos 02 - 02 José Roberto }

# Black: }
# w: José Roberto 00 - 11 Jefferson Campos }
# l: José Roberto 07 - 00 Jefferson Campos }
# d: José Roberto 01 - 01 Jefferson Campos }
# *: José Roberto 01 - 01 Jefferson Campos }

# jeff 28 - 14 josé roberto }

# ------------------

# white:
# w: jeff 03 - 00 jose carlos bento
# l: jeff 00 - 03 jose carlos bento
# d: jeff 00 - 00 jose carlos bento
# *: jeff 02 - 02 jose carlos bento

# jeff 3 - 3 jose carlos

# black:
# w: jose carlos bento 00 - 03 jeff
# l: jose carlos bento 02 - 00 jeff
# d: jose carlos bento 00 - 00 jeff
# *: jose carlos bento 07 - 07 jeff

# jose carlos 02 - 03 jeff

# jeff 6x5
