import chess.pgn
import os
import csv
import logging
from collections import OrderedDict
from pprint import pprint
from prettytable import PrettyTable
from util import Util
from game import GameResult
from player import OpponentStats

def padoca_championship_2022_02():
    # TODO calc keys instead hard code it! }
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

def my_games():
    # TODO implement more detailed analisys
    total_errors = 0
    total_games = 0
    total_win_loss = 0
    total_draws = 0
    unfinished = 0
    unknow_opponent = 0
    undefined_opponents = 0

    # TODO calc keys instead of hard code it!
    leader_board = {
        "Emerson Sbrana": OpponentStats("Emerson Sbrana"),
        "Isac Nunes": OpponentStats("Isac Nunes"),
        "Ivone Xadrez": OpponentStats("Ivone Xadrez"),
        "Jefferson Nunes": OpponentStats("Jefferson Nunes"),
        "Jessé Garcia Galiano": OpponentStats("Jessé Garcia Galiano"),
        "José Carlos Bento Dias da Rocha": OpponentStats("José Carlos Bento Dias da Rocha"),
        "José Roberto Oliveira": OpponentStats("José Roberto Oliveira"),
        "João Carlos Oliveira": OpponentStats("João Carlos Oliveira"),
        "Mário Sérgio Bueno de Miranda": OpponentStats("Mário Sérgio Bueno de Miranda"),
        "?": OpponentStats("?")
    }

    with open("data/jeff_stats.csv", "w") as s:
        writer = csv.writer(s, delimiter = ";")
        writer.writerow(["timestamp", "white", "black", "result"])
        for path in os.listdir("data/pgn/mgr/"):
            with open("data/pgn/mgr/" + path, encoding = "utf-8") as pgn:
                total_games += 1
                game = chess.pgn.read_game(pgn)
                game_result = GameResult(game.headers["Date"], game.headers["White"], game.headers["Black"], game.headers["Result"])

                if len(game.errors) != 0:
                    logging.info(Util.error("file: {f}".format(f = path)))
                    total_errors += 1

                writer.writerow([game.headers["Date"], game.headers["White"], game.headers["Black"], game.headers["Result"]])
                if game.headers["Result"] == "1-0" or game.headers["Result"] == "0-1":
                    total_win_loss += 1
                elif game.headers["Result"] == "1/2-1/2":
                    total_draws += 1
                elif game.headers["Result"] == "*":
                    unfinished += 1

                if game_result.is_against("?"):
                    unknow_opponent += 1

                if not game_result.is_undefined_game():
                    try:
                        leader_board[game.headers[game_result.opponent_color()]].count_result(game_result)
                    except Exception as e:
                        logging.error(Util.error("My games failed! {p}".format(p = path)))
                        logging.error(Util.error(e))
                else:
                    undefined_opponents += 1

    ptable = PrettyTable()
    ptable.field_names = ['TOTAL GAMES', 'WIN/LOSS', 'DRAWS', 'UNFINISHED', 'ERRORS', 'UNKNOW GAMES', 'UNDEFINED OPPONENTS']
    ptable.add_row([total_games, total_win_loss, total_draws, unfinished, total_errors, unknow_opponent, undefined_opponents])
    print(ptable)
    logging.debug(Util.info("total_games: {g} - total_win_loss: {f} - total unfinished: {u} - total_draw:{d} - unknow_opponent: {k} - undefined_opponents: {o} - total_errors: {e}".format(u = unfinished, e = total_errors, g = total_games, f = total_win_loss, d = total_draws, k = unknow_opponent, o = undefined_opponents)))

    leader_board_table = PrettyTable()
    leader_board_table.field_names = [
        'Player',
        'W Wins',
        'B Wins',
        'T Wins',
        'W Losses',
        'B Losses',
        'T Losses',
        'W Draws',
        'B Draws',
        'T Draws',
        'W Unfin',
        'B Unfin',
        'T Unfin',
        'W Games',
        'B Games',
        'T Games'
    ]
    
    for key, player in leader_board.items():
        leader_board_table.add_row([
            player.name,
            player.white["wins"],
            player.black["wins"],
            player.white["wins"] + player.black["wins"],
            player.white["losses"],
            player.black["losses"],
            player.white["losses"] + player.black["losses"],
            player.white["draws"],
            player.black["draws"],
            player.white["draws"] + player.black["draws"],
            player.white["unfinished"],
            player.black["unfinished"],
            player.white["unfinished"] + player.black["unfinished"],
            player.white["wins"] + player.white["losses"] + player.white["draws"] + player.white["unfinished"],
            player.black["wins"] + player.black["losses"] + player.black["draws"] + player.black["unfinished"],
            (player.white["wins"] + player.black["wins"]) + (player.white["losses"] + player.black["losses"]) + (player.white["draws"] + player.black["draws"]) + (player.white["unfinished"] + player.black["unfinished"])
        ])
    
    print(leader_board_table)

def debug_game(game):
    logging.debug(Util.debug("Game was: {g}".format(g = game)))
    with open("data/pgn/mgr/{g}.pgn".format(g = game), encoding = "utf-8") as pgn:
        game = chess.pgn.read_game(pgn)
        print(len(game.errors), game.errors)
        print(game)
