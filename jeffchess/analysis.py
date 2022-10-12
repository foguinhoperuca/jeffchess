import chess.pgn
import os
import csv
import logging
from collections import OrderedDict
from pprint import pprint
from prettytable import PrettyTable, ORGMODE
from prettytable.colortable import ColorTable, Themes
from util import Util
from game import GameResult
from player import OpponentStats

def padoca_championship(championship_data_file = "stats.csv"):
    # TODO calc keys instead hard code it! }
    with open(f"data/{championship_data_file}") as stats:
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
            "Rodrigo Guimarães de Azevedo": {
                "points": 0,
                "unfinished": 0
            },
            "Erick de Brito Melo": {
                "points": 0,
                "unfinished": 0
            }
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
        "Rodrigo Guimarães de Azevedo": OpponentStats("Rodrigo de Guimarães Azevedo"),
        "Erick de Brito Melo": OpponentStats("Erick de Brito Melo"),
        "?": OpponentStats("?")
    }

    with open("data/jeff_stats.csv", "w") as s:
        writer = csv.writer(s, delimiter = ";")
        writer.writerow(["timestamp", "white", "black", "result", "filename"])
        for path in os.listdir("data/pgn/mgr/"):
            with open("data/pgn/mgr/" + path, encoding = "utf-8") as pgn:
                total_games += 1
                game = chess.pgn.read_game(pgn)
                game_result = GameResult(game.headers["Date"], game.headers["White"], game.headers["Black"], game.headers["Result"], path)

                if len(game.errors) != 0:
                    logging.info(Util.error("file: {f}".format(f = path)))
                    total_errors += 1

                # if path == "2018-10-23T21-12-54.pgn":
                #     print("..............................")
                #     print(f'game.headers["Date"]: {game.headers["Date"]!#\')
                #     print(f'game.headers["White"]: {game.headers["White"]!#\')
                #     print(f'game.headers["Black"]: {game.headers["Black"]!#\')
                #     print(f'game.headers["Result"]: {game.headers["Result"]!#\')
                #     print(f'path: {path!#\')
                #     print(len(game.errors), game.errors)
                #     print(game)
                #     print("..............................")

                writer.writerow([game.headers["Date"], game.headers["White"], game.headers["Black"], game.headers["Result"], path])
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

    # TODO get more themes
    leader_board_table = ColorTable(theme=Themes.OCEAN) # PrettyTable()
    # leader_board_table.set_style(ORGMODE) # only works with PrettyTable
    leader_board_table.field_names = [
        'Player',
        'W W', # 'W Wins',
        'B W', # 'B Wins',
        'T W', # 'T Wins',
        'W L', # 'W Losses',
        'B L', # 'B Losses',
        'T L', # 'T Losses',
        'W D', # 'W Draws',
        'B D', # 'B Draws',
        'T D', # 'T Draws',
        'W U', # 'W Unfin',
        'B U', # 'B Unfin',
        'T U', # 'T Unfin',
        'W G', # 'W Games',
        'B G', # 'B Games',
        'T G'  # 'T Games'
    ]
    leader_board_table.align["Player"] = "l"

    total_white_wins = 0
    total_black_wins = 0
    total_wins = 0
    total_white_losses = 0
    total_black_losses = 0
    total_losses = 0
    total_white_draws = 0
    total_black_draws = 0
    total_draws = 0
    total_white_unfinished = 0
    total_black_unfinished = 0
    total_unfinished = 0
    total_white_games = 0
    total_black_games = 0
    total_games = 0
    for key, player in leader_board.items():
        total_white_wins += player.white["wins"]
        total_black_wins += player.black["wins"]
        total_wins += player.white["wins"] + player.black["wins"]
        total_white_losses += player.white["losses"]
        total_black_losses += player.black["losses"]
        total_losses += player.white["losses"] + player.black["losses"]
        total_white_draws += player.white["draws"]
        total_black_draws += player.black["draws"]
        total_draws += player.white["draws"] + player.black["draws"]
        total_white_unfinished += player.white["unfinished"]
        total_black_unfinished += player.black["unfinished"]
        total_unfinished += player.white["unfinished"] + player.black["unfinished"]
        total_white_games += player.white["wins"] + player.white["losses"] + player.white["draws"] + player.white["unfinished"]
        total_black_games += player.black["wins"] + player.black["losses"] + player.black["draws"] + player.black["unfinished"]
        total_games += (player.white["wins"] + player.black["wins"]) + (player.white["losses"] + player.black["losses"]) + (player.white["draws"] + player.black["draws"]) + (player.white["unfinished"] + player.black["unfinished"])

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

    leader_board_table.add_row([
        "-------------------------------",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--",
        "--"
    ])
    leader_board_table.add_row([
        "TOTAL",
        total_white_wins,
        total_black_wins,
        total_wins,
        total_white_losses,
        total_black_losses,
        total_losses,
        total_white_draws,
        total_black_draws,
        total_draws,
        total_white_unfinished,
        total_black_unfinished,
        total_unfinished,
        total_white_games,
        total_black_games,
        total_games
    ])
    print(leader_board_table)
    print("A B --> (A) [White | Black | Total]; (B) [Wins | Losses | Draws | Unfinished | Games]")

def debug_game(game):
    logging.debug(Util.debug("Game was: {g}".format(g = game)))
    with open("data/pgn/mgr/{g}.pgn".format(g = game), encoding = "utf-8") as pgn:
        game = chess.pgn.read_game(pgn)
        print(len(game.errors), game.errors)
        print(game)

def extract_opponent_from_my_games(player = "Jefferson Campos"):
    pass

def extract_players_from_championship(championship_data_file = "stats.csv"):
    pass
