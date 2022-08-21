import chess.pgn
import os
import csv
import logging
from collections import OrderedDict
from pprint import pprint
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
            # print("white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
            # if row[1] == "Jefferson Campos" or row[2] == "Jefferson Campos":
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

        return od

# TODO implement  more detailed analisys
# championship.ods #	Player	White	Black	Total	Unfinished	JUN/2022	JUL/2022	AUG/2022

def my_games():
    unfinished = 0
    total_errors = 0
    total_games = 0
    for path in os.listdir("data/pgn/mgr/"):
        with open("data/pgn/mgr/" + path, encoding = "utf-8") as pgn:
            total_games += 1
            game = chess.pgn.read_game(pgn)
            if len(game.errors) != 0:
                print(Util.error("file: {f}".format(f = path)))
                total_errors += 1

            # print("--------------------------------------------") }
            if game.headers["Result"] == "*":
                # print("file: {f!#\ white: {w!#\ black: {b!#\ result: {r!#\".format(f = path, w = game.headers["White"], b = game.headers["Black"], r = game.headers["Result"])) }
                unfinished += 1

    print("Total unfinished: {u} - total_errors: {e} - total_games: {g}".format(u = unfinished, e = total_errors, g = total_games))


def manual_load(game):
    print("Game was: {g}".format(g = game))
    with open("data/pgn/mgr/{g}.pgn".format(g = game), encoding = "utf-8") as pgn:
        game = chess.pgn.read_game(pgn)
        print("*****************")
        print(game.errors)
        print(len(game.errors))
        
# 2020-01-07T22-01-49
# 2020-01-14T21-58-09
