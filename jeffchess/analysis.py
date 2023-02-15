import chess.pgn
import os
import csv
import logging
from collections import OrderedDict
from pprint import pprint
from prettytable import PrettyTable, ORGMODE, ALL
from prettytable.colortable import ColorTable, Themes
from util import Util
from game import GameResult
from player import OpponentStats

ALL_PLAYERS = [
    "Jefferson Campos",
    "Emerson Sbrana",
    "José Carlos Bento Dias da Rocha",
    "Jefferson Nunes",
    "João Carlos Oliveira",
    "Mário Sérgio Bueno Miranda",
    "José Roberto Oliveira",
    "Erick de Brito Melo",
    "Rodrigo Guimarães de Azevedo",
    "Vicente Rodrigues de Moraes"
]

ALL_PLAYERS_NAME_NICKNAMES = {
    "Jefferson Campos":                "Jefferson Campos ",
    "Emerson Sbrana":                  "Emerson Sbrana   ",
    "José Carlos Bento Dias da Rocha": "José C B D Rocha ",
    "Jefferson Nunes":                 "Jefferson Nunes  ",
    "João Carlos Oliveira":            "João C Oliveira  ",
    "Mário Sérgio Bueno Miranda":      "Mário S B Miranda",
    "José Roberto Oliveira":           "José R Oliveira  ",
    "Erick de Brito Melo":             "Erick Brito Melo ",
    "Rodrigo Guimarães de Azevedo":    "Rodrigo G Azevedo",
    "Vicente Rodrigues de Moraes":     "Vicente R Moraes ",
    "BY PLAYER":                       "--- BY PLAYER ---",
}

INFREQUENT_PLAYERS = [
    "Mário Sérgio Bueno Miranda",
    "Erick de Brito Melo",
    "Rodrigo Guimarães de Azevedo",
    "Vicente Rodrigues de Moraes"
]

def games_by_player(choosen_player='Jefferson Campos', infrequent_players=False):
    total_games_white = 0
    total_missing_white = 0
    total_games_black = 0
    total_missing_black = 0
    players_table = ColorTable(theme=Themes.OCEAN) # PrettyTable()
    # players_table.hrules = ALL
    players_table.field_names = [
        'Round',
        'White',
        'Result',
        'Black',
        'Date'
    ]

    if not infrequent_players:
        # players = list(filter(lambda p: p != choosen_player, ALL_PLAYERS))
        players = list(filter(lambda player: player not in INFREQUENT_PLAYERS and player != choosen_player, ALL_PLAYERS))
    else:
        players = list(filter(lambda p: p != choosen_player, ALL_PLAYERS))

    logging.debug("players {p}".format(p=players))
    logging.info(f"{choosen_player = }")

    with open(f"data/padoca_cup_2022.csv", encoding="UTF-8") as stats:
        games_choosen_player = list(filter(lambda row: (row[1] == choosen_player or row[2] == choosen_player), csv.reader(stats, delimiter = ';')))

    for index, player in enumerate(players):
        game = list(filter(lambda g: g[1] == choosen_player and g[2] == player, games_choosen_player))
        if len(game) > 0:
            round_played = index + 1
            white = choosen_player
            black = player
            game_result = game[0][3]
            game_date = game[0][0]
            total_games_white += 1
        else:
            round_played = Util.emphasys(index + 1)
            white = Util.emphasys(choosen_player)
            black = Util.emphasys(player)
            game_result = Util.emphasys('?-?')
            game_date = Util.emphasys('YYYY-MM-DD')
            total_missing_white += 1

        players_table.add_row([round_played, white, game_result, black, game_date])

    players_table.add_row(['-----', '-----', '-----', '-----', '-----'])

    for index, player in enumerate(players):
        game = list(filter(lambda g: g[1] == player and g[2] == choosen_player, games_choosen_player))
        if len(game) > 0:
            round_played = len(players) + (index + 1)
            white = player
            black = choosen_player
            game_result = game[0][3]
            game_date = game[0][0]
            total_games_black += 1
        else:
            round_played = Util.emphasys(len(players) + (index + 1))
            white = Util.emphasys(player)
            black = Util.emphasys(choosen_player)
            game_result = Util.emphasys('?-?')
            game_date = Util.emphasys('YYYY-MM-DD')
            total_missing_black += 1

        players_table.add_row([round_played, white, game_result, black, game_date])

    # print(players_table.get_html_string())
    print(players_table)
    print(Util.white_piece(f"{total_games_white = } {total_missing_white = }"))
    print(Util.black_piece(f"{total_games_black = } {total_missing_black = }"))

def generate_pairing_tables(championship_data_file="padoca_cup_2022.csv", infrequent_players=False):
    if not infrequent_players:
        players = list(filter(lambda player: player not in INFREQUENT_PLAYERS, ALL_PLAYERS))
    else:
        players = ALL_PLAYERS

    logging.debug("players {p}".format(p=players))

    if len(players) % 2 == 1:
        players.insert((int(len(players) / 2) + 1), 'BY PLAYER')

    middle = int(len(players) / 2)
    up = players[0:middle]
    down = players[middle:len(players)]

    with open(f"data/padoca_cup_2022.csv", encoding="UTF-8") as stats:
        games = list(csv.reader(stats, delimiter = ';'))

    for match_game in range(1, len(players), 1):
        print(f"Match #{match_game}")
        match_table = ColorTable(theme=Themes.OCEAN)
        match_table.field_names = [
            'Match',
            Util.white_piece('White (1)'),
            'Result (1)',
            Util.black_piece('Black (1)'),
            'Date (1)',
            Util.white_piece('White (2)'),
            'Result (2)',
            Util.black_piece('Black (2)'),
            'Date (2)'
        ]

        for index, player in enumerate(up):
            match_game_tbl = Util.warning(match_game) if index == 0 else ''
            if player == 'BY PLAYER' or down[index] == 'BY PLAYER':
                not_played_yet = [Util.player_named_by('YYYY-MM-DD'), player, down[index], Util.player_named_by('?-?'), 'Not played yet!']
                white_1 = Util.player_named_by(f' {ALL_PLAYERS_NAME_NICKNAMES[player]} ')
                black_1 = Util.player_named_by(f' {ALL_PLAYERS_NAME_NICKNAMES[down[index]]} ')
                white_2 = Util.player_named_by(f' {ALL_PLAYERS_NAME_NICKNAMES[down[index]]} ')
                black_2 = Util.player_named_by(f' {ALL_PLAYERS_NAME_NICKNAMES[player]} ')
            else:
                not_played_yet = [Util.emphasys('YYYY-MM-DD'), player, down[index], Util.emphasys('?-?'), 'Not played yet!']
                white_1 = Util.white_piece(f' {ALL_PLAYERS_NAME_NICKNAMES[player]} ')
                black_1 = Util.black_piece(f' {ALL_PLAYERS_NAME_NICKNAMES[down[index]]} ')
                white_2 = Util.white_piece(f' {ALL_PLAYERS_NAME_NICKNAMES[down[index]]} ')
                black_2 = Util.black_piece(f' {ALL_PLAYERS_NAME_NICKNAMES[player]} ')

            game_1 = list(filter(lambda row: row[1] == player and row[2] == down[index], games))
            g1 = game_1[0] if len(game_1) > 0 else not_played_yet

            game_2 = list(filter(lambda row: row[1] == down[index] and row[2] == player, games))
            g2 = game_2[0] if len(game_2) > 0 else not_played_yet

            match_table.add_row([match_game_tbl, white_1, g1[3], black_1, g1[0], white_2, g2[3], black_2, g2[0]])

        print(match_table)

        tail = up.pop(len(up) - 1)
        down.insert(len(down), tail)
        head = down.pop(0)
        up.insert(1, head)

# FIXME draws isn't working - See José Carlos Bento Dias da Rocha
def padoca_championship(championship_data_file="stats.csv", set_unfinished_column=True, infrequent_players=False):
    with open(f"data/{championship_data_file}", encoding="UTF-8") as stats:
        csv_reader = csv.reader(stats, delimiter = ';')
        total_games = 0
        gemes_jump = 0
        classification = {}
        players = ALL_PLAYERS
        if not infrequent_players:
            players = list(filter(lambda player: player not in INFREQUENT_PLAYERS, ALL_PLAYERS))

        for player in players:
            classification[f"{player}"] = {
                "points": 0,
                "unfinished": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "total_games": 0,
                "lost_points": 0
            }

        for row in csv_reader:
            if total_games == 0:
                total_games = 1
                continue

            if row[1] in INFREQUENT_PLAYERS or row[2] in INFREQUENT_PLAYERS:
                gemes_jump += 1
                continue

            total_games += 1
            match row[3]:
                case "1-0":
                    logging.debug("white wins! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[1]]["points"] += 1
                    classification[row[1]]["wins"] += 1
                    classification[row[2]]["losses"] += 1
                    classification[row[1]]["total_games"] += 1
                    classification[row[2]]["total_games"] += 1
                    classification[row[2]]["lost_points"] += 1
                case "0-1":
                    logging.debug("black wins! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[2]]["points"] += 1
                    classification[row[2]]["wins"] += 1
                    classification[row[1]]["losses"] += 1
                    classification[row[2]]["total_games"] += 1
                    classification[row[1]]["total_games"] += 1
                    classification[row[1]]["lost_points"] += 1
                case "0,5-0,5":
                    logging.debug("draw! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[1]]["points"] += 0.5
                    classification[row[2]]["points"] += 0.5
                    classification[row[1]]["draws"] += 1
                    classification[row[2]]["draws"] += 1
                    classification[row[1]]["total_games"] += 1
                    classification[row[2]]["total_games"] += 1
                    classification[row[1]]["lost_points"] += 0.5
                    classification[row[2]]["lost_points"] += 0.5
                case "*":
                    logging.debug("unfinished! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))
                    classification[row[1]]["unfinished"] += 1
                    classification[row[2]]["unfinished"] += 1
                    classification[row[1]]["total_games"] += 1
                    classification[row[2]]["total_games"] += 1
                case _:
                    logging.debug("got an invalid value! white: {w} - black {b} - result: {r}".format(w = row[1], b = row[2], r = row[3]))

        logging.info(Util.info("total games: {t}".format(t = total_games)))

        od = OrderedDict(sorted(classification.items(), key = lambda x: x[1]["points"], reverse = True))
        ptable = PrettyTable()
        if set_unfinished_column:
            ptable.field_names = ['Clas', 'Player', 'Points', 'Unfinished', 'Wins', 'Losses', 'Draws', 'Total Games', 'Lost Points']
        else:
            ptable.field_names = ['Clas', 'Player', 'Points', 'Wins', 'Losses', 'Draws', 'Total Games', 'Lost Points']

        position = 1
        for key, value in od.items():
            points, unfinished, wins, losses, draws, total_games, lost_points = value.items()
            if set_unfinished_column:
                ptable.add_row([position, key, points[1], unfinished[1], wins[1], losses[1], draws[1], total_games[1], lost_points[1]])
            else:
                ptable.add_row([position, key, points[1], wins[1], losses[1], draws[1], total_games[1], lost_points[1]])

            position += 1

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
        "Vicente Rodrigues de Moraes": OpponentStats("Vicente Rodrigues de Moraes"),
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

def generate_list_my_games(opponent, show_full_games=True):
    logging.info(Util.debug("opponent was: {o}".format(o = opponent)))

    games = []
    total_games = 0
    headers = [
        'Game #',
        'Date',
        'White',
        'Result',
        'Black',
        'Path'
    ]
    tbl = ColorTable(theme=Themes.OCEAN)
    tbl.field_names = headers
    # tbl.hrules = ALL
    tbl_open = ColorTable(theme=Themes.OCEAN)
    tbl_open.field_names = headers

    for path in os.listdir("data/pgn/mgr/"):
        with open("data/pgn/mgr/" + path, encoding = "utf-8") as pgn:
            total_games += 1
            game = chess.pgn.read_game(pgn)
            if game.headers["White"] == opponent or game.headers["Black"] == opponent:
                games.extend([(game.headers["Date"], game.headers["White"], game.headers["Result"], game.headers["Black"], path)])

            # if len(game.errors) != 0:
            #     logging.info(Util.error("file: {f!#\".format(f = path)))
            #     total_errors += 1

    games.sort(key=lambda e: e[0])

    for index, g in enumerate(games):
        tbl.add_row([(index + 1), g[0], g[1], g[2], g[3], g[4]])

    for index, g in enumerate(list(filter(lambda g: g[2] == "*", games))):
        tbl_open.add_row([(index + 1), g[0], g[1], g[2], g[3], g[4]])

    if show_full_games:
        print(tbl)

    print(tbl_open)

def extract_opponent_from_my_games(player = "Jefferson Campos"):
    pass

def extract_players_from_championship(championship_data_file = "stats.csv"):
    pass
