from abc import ABCMeta, ABC
import chess.pgn
from collections import OrderedDict
import csv
from datetime import datetime
import logging
import math
import os
from typing import Dict, List, Optional, Tuple

from prettytable import PrettyTable  # , ORGMODE, ALL
from prettytable.colortable import ColorTable, Themes

from util import Util
from game import GameResult, ResultType
from player import OpponentStats


class Analysis(metaclass=ABCMeta):
    DEFAULT_PLAYER_DATA_FILE: str = "data/players.csv"
    BY_PLAYER: Dict[str, str] = {
        "real_name": "BY PLAYER",
        "lichess.org": "",
        "nickname": "--- BY PLAYER ---",
        "infrequent": "True"
    }
    # def __init__(self):
    #     self._logger = Util.logger_factory()

    # @property
    # def logger(self):
    #     return self._logger

    def debug_game(self, game):
        logging.debug(Util.debug("Game was: {g}".format(g=game)))
        with open("data/pgn/mgr/{g}.pgn".format(g=game), encoding="utf-8") as pgn:
            game = chess.pgn.read_game(pgn)
            print(len(game.errors), game.errors)
            print(game)

    def get_players(self, get_infrequents: bool = False) -> List:
        players: List
        with open(Analysis.DEFAULT_PLAYER_DATA_FILE, encoding="UTF-8") as players_data_file:
            csv_reader = csv.DictReader(players_data_file, delimiter=";")
            players = [player for player in csv_reader] if get_infrequents else [player for player in csv_reader if player["infrequent"] == "False"]

        if (len(players) % 2) == 1:
            players.append(Analysis.BY_PLAYER)

        return players

    def get_infrequent_players(self) -> List:
        players: List
        with open(Analysis.DEFAULT_PLAYER_DATA_FILE, encoding="UTF-8") as players_data_file:
            csv_reader = csv.DictReader(players_data_file, delimiter=";")
            players = [player for player in csv_reader if player["infrequent"] == "True"]

        return players


class Championship(Analysis, ABC):
    DEFAULT_CHAMPIONSHIP_DATA_FILE: str = "data/padoca-cup.csv"

    # FIXME draws isn't working - See José Carlos Bento Dias da Rocha
    def championship_lead_border(self, championship_data_file: str = DEFAULT_CHAMPIONSHIP_DATA_FILE, set_unfinished_column: bool = True, infrequent_players: bool = False) -> None:
        with open(f"{championship_data_file}", encoding="UTF-8") as stats:
            csv_reader = csv.reader(stats, delimiter=';')
            total_games = 0
            games_jump = 0
            classification = {}
            players = self.get_players(get_infrequents=infrequent_players)
            infrequent_players = [player["real_name"] for player in self.get_infrequent_players()]

            for player in players:
                classification[f"{player['real_name']}"] = {
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

                if row[1] in infrequent_players or row[2] in infrequent_players:
                    games_jump += 1
                    continue

                total_games += 1
                match row[3]:
                    case "1-0":
                        logging.debug("white wins! white: {w} - black {b} - result: {r}".format(w=row[1], b=row[2], r=row[3]))
                        classification[row[1]]["points"] += 1
                        classification[row[1]]["wins"] += 1
                        classification[row[2]]["losses"] += 1
                        classification[row[1]]["total_games"] += 1
                        classification[row[2]]["total_games"] += 1
                        classification[row[2]]["lost_points"] += 1
                    case "0-1":
                        logging.debug("black wins! white: {w} - black {b} - result: {r}".format(w=row[1], b=row[2], r=row[3]))
                        classification[row[2]]["points"] += 1
                        classification[row[2]]["wins"] += 1
                        classification[row[1]]["losses"] += 1
                        classification[row[2]]["total_games"] += 1
                        classification[row[1]]["total_games"] += 1
                        classification[row[1]]["lost_points"] += 1
                    case "0,5-0,5":
                        logging.debug("draw! white: {w} - black {b} - result: {r}".format(w=row[1], b=row[2], r=row[3]))
                        classification[row[1]]["points"] += 0.5
                        classification[row[2]]["points"] += 0.5
                        classification[row[1]]["draws"] += 1
                        classification[row[2]]["draws"] += 1
                        classification[row[1]]["total_games"] += 1
                        classification[row[2]]["total_games"] += 1
                        classification[row[1]]["lost_points"] += 0.5
                        classification[row[2]]["lost_points"] += 0.5
                    case "*":
                        logging.debug("unfinished! white: {w} - black {b} - result: {r}".format(w=row[1], b=row[2], r=row[3]))
                        classification[row[1]]["unfinished"] += 1
                        classification[row[2]]["unfinished"] += 1
                        classification[row[1]]["total_games"] += 1
                        classification[row[2]]["total_games"] += 1
                    case _:
                        logging.debug("got an invalid value! white: {w} - black {b} - result: {r}".format(w=row[1], b=row[2], r=row[3]))

            logging.info(Util.info("total games: {t}".format(t=total_games)))

            od = OrderedDict(sorted(classification.items(), key=lambda x: x[1]["points"], reverse=True))
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

            logging.debug(Util.debug("args: {v}".format(v=od)))
            print(ptable)

    def games_by_player(self, choosen_player='Jefferson Campos', infrequent_players=False) -> None:
        """Análise do Campeonato da Padoca 2022 - ótica de um dos jogadores"""
        total_games_white: int = 0
        total_missing_white: int = 0
        total_games_black: int = 0
        total_missing_black: int = 0
        players_table: ColorTable = ColorTable(theme=Themes.OCEAN)  # PrettyTable()
        # players_table.hrules = ALL
        players_table.field_names = [
            'Round',
            'White',
            'Result',
            'Black',
            'Date'
        ]

        players = self.get_players(get_infrequents=infrequent_players)
        logging.debug("players {p}".format(p=players))
        logging.info(f"{choosen_player = }")

        with open(f"{Championship.DEFAULT_CHAMPIONSHIP_DATA_FILE}", encoding="UTF-8") as stats:
            games_choosen_player = list(filter(lambda row: (row[1] == choosen_player or row[2] == choosen_player), csv.reader(stats, delimiter=';')))

        for index, player in enumerate(players):
            game = list(filter(lambda g: g[1] == choosen_player and g[2] == player["real_name"], games_choosen_player))
            if len(game) > 0:
                round_played = index + 1
                white = choosen_player
                black = player["real_name"]
                game_result = game[0][3]
                game_date = game[0][0]
                total_games_white += 1
            else:
                round_played = Util.emphasys(index + 1)
                white = Util.emphasys(choosen_player)
                black = Util.emphasys(player["real_name"])
                game_result = Util.emphasys('?-?')
                game_date = Util.emphasys('YYYY-MM-DD')
                total_missing_white += 1

            players_table.add_row([round_played, white, game_result, black, game_date])

        players_table.add_row(['-----', '-----', '-----', '-----', '-----'])

        for index, player in enumerate(players):
            game = list(filter(lambda g: g[1] == player["real_name"] and g[2] == choosen_player, games_choosen_player))
            if len(game) > 0:
                round_played = len(players) + (index + 1)
                white = player["real_name"]
                black = choosen_player
                game_result = game[0][3]
                game_date = game[0][0]
                total_games_black += 1
            else:
                round_played = Util.emphasys(len(players) + (index + 1))
                white = Util.emphasys(player["real_name"])
                black = Util.emphasys(choosen_player)
                game_result = Util.emphasys('?-?')
                game_date = Util.emphasys('YYYY-MM-DD')
                total_missing_black += 1

            players_table.add_row([round_played, white, game_result, black, game_date])

        # print(players_table.get_html_string())
        print(players_table)
        print(Util.white_piece(f"{total_games_white = } {total_missing_white = }"))
        print(Util.black_piece(f"{total_games_black = } {total_missing_black = }"))

    def generate_pairing_tables(self, infrequent_players: bool = False) -> None:
        """Combine a list of players to generate a table game"""

        players = self.get_players(get_infrequents=infrequent_players)
        middle = int(len(players) / 2)
        up = players[0:middle]
        down = players[middle:len(players)]

        with open(f"{Championship.DEFAULT_CHAMPIONSHIP_DATA_FILE}", encoding="UTF-8") as stats:
            games = list(csv.reader(stats, delimiter=';'))

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
                if player["real_name"] == 'BY PLAYER' or down[index]["real_name"] == 'BY PLAYER':
                    not_played_yet = [Util.player_named_by('YYYY-MM-DD'), player, down[index], Util.player_named_by('?-?'), 'Not played yet!']
                    white_1 = Util.player_named_by(f' {player["nickname"]} ')
                    black_1 = Util.player_named_by(f' {down[index]["nickname"]} ')
                    white_2 = Util.player_named_by(f' {down[index]["nickname"]} ')
                    black_2 = Util.player_named_by(f' {player["nickname"]} ')
                else:
                    not_played_yet = [Util.emphasys('YYYY-MM-DD'), player, down[index], Util.emphasys('?-?'), 'Not played yet!']
                    white_1 = Util.white_piece(f' {player["nickname"]} ')
                    black_1 = Util.black_piece(f' {down[index]["nickname"]} ')
                    white_2 = Util.white_piece(f' {down[index]["nickname"]} ')
                    black_2 = Util.black_piece(f' {player["nickname"]} ')

                game_1 = list(filter(lambda row: row[1] == player["real_name"] and row[2] == down[index]["real_name"], games))
                g1 = game_1[0] if len(game_1) > 0 else not_played_yet

                game_2 = list(filter(lambda row: row[1] == down[index]["real_name"] and row[2] == player["real_name"], games))
                g2 = game_2[0] if len(game_2) > 0 else not_played_yet

                match_table.add_row([match_game_tbl, white_1, g1[3], black_1, g1[0], white_2, g2[3], black_2, g2[0]])

            print(match_table)

            tail = up.pop(len(up) - 1)
            down.insert(len(down), tail)
            head = down.pop(0)
            up.insert(1, head)

    def stats(self, player: Optional[str]) -> None:
        self.championship_lead_border(championship_data_file=Championship.DEFAULT_CHAMPIONSHIP_DATA_FILE)
        if player is not None:
            self.games_by_player(choosen_player=player)
        else:
            self.generate_pairing_tables()


class PersonalAnaysis(Analysis, ABC):
    MYSELF: str = "Jefferson Campos"
    DEFAULT_INITIAL_RATING: float = 1000.0

    def define_leader_board(self, opponent: Optional[str]) -> dict:
        leader_board = dict()
        if opponent is None:
            with open('data/players.csv') as players:
                next(players)
                for row in csv.reader(players, delimiter=';'):
                    if row[0] == PersonalAnaysis.MYSELF:
                        continue

                    leader_board[row[0]] = OpponentStats(row[0])

            leader_board["?"] = OpponentStats("?")
        else:
            leader_board[opponent] = OpponentStats(opponent)

        return leader_board

    def my_games(self, opponent: Optional[str] = None, games_played: Optional[List] = None) -> None:
        total_errors = 0
        total_files = 0

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

        unknow_opponent = 0
        undefined_opponents = 0

        leader_board = self.define_leader_board(opponent)
        games = []
        games_files: List = games_played if games_played is not None else os.listdir("data/pgn/mgr/")

        for path in games_files:
            with open("data/pgn/mgr/" + path, encoding="utf-8") as pgn:
                total_files += 1
                game = chess.pgn.read_game(pgn)

                if len(game.errors) != 0:
                    logging.info(Util.error("file: {f}".format(f=path)))
                    total_errors += 1

                game_result = GameResult(game.headers["Date"], game.headers["White"], game.headers["Black"], game.headers["Result"], path)
                if opponent is not None:
                    if game.headers["White"] != opponent and game.headers["Black"] != opponent:
                        continue

                    games.extend([(game.headers["Date"], game.headers["White"], game.headers["Result"], game.headers["Black"], path)])
                else:
                    if game_result.is_against("?"):
                        unknow_opponent += 1

                    if game_result.is_undefined_game():
                        undefined_opponents += 1

                if not game_result.is_undefined_game():
                    try:
                        leader_board[game.headers[game_result.opponent_color()]].count_result(game_result)
                    except Exception as e:
                        logging.error(Util.error("My games failed! {p}".format(p=path)))
                        logging.error(Util.error(e))

        leader_board_table = ColorTable(theme=Themes.OCEAN)  # PrettyTable()
        # leader_board_table.set_style(ORGMODE) # only works with PrettyTable
        leader_board_table.field_names = [
            'Player',
            'W W',  # 'W Wins',
            'B W',  # 'B Wins',
            'T W',  # 'T Wins',
            'W L',  # 'W Losses',
            'B L',  # 'B Losses',
            'T L',  # 'T Losses',
            'W D',  # 'W Draws',
            'B D',  # 'B Draws',
            'T D',  # 'T Draws',
            'W U',  # 'W Unfin',
            'B U',  # 'B Unfin',
            'T U',  # 'T Unfin',
            'W G',  # 'W Games',
            'B G',  # 'B Games',
            'T G'   # 'T Games'
        ]
        leader_board_table.align["Player"] = "l"
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
                Util.emphasys(player.white["wins"] + player.black["wins"]),
                player.white["losses"],
                player.black["losses"],
                Util.emphasys(player.white["losses"] + player.black["losses"]),
                player.white["draws"],
                player.black["draws"],
                Util.emphasys(player.white["draws"] + player.black["draws"]),
                player.white["unfinished"],
                player.black["unfinished"],
                Util.emphasys(player.white["unfinished"] + player.black["unfinished"]),
                player.white["wins"] + player.white["losses"] + player.white["draws"] + player.white["unfinished"],
                player.black["wins"] + player.black["losses"] + player.black["draws"] + player.black["unfinished"],
                Util.emphasys((player.white["wins"] + player.black["wins"]) + (player.white["losses"] + player.black["losses"]) + (player.white["draws"] + player.black["draws"]) + (player.white["unfinished"] + player.black["unfinished"]))
            ])

        if opponent is not None:
            games.sort(key=lambda e: e[0])
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

            for index, g in enumerate(games):
                tbl.add_row([(index + 1), g[0], g[1], g[2], g[3], g[4]])

            for index, g in enumerate(list(filter(lambda g: g[2] == "*", games))):
                tbl_open.add_row([(index + 1), g[0], g[1], g[2], g[3], g[4]])
        else:
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
                Util.player_named_by(total_wins),
                total_white_losses,
                total_black_losses,
                Util.player_named_by(total_losses),
                total_white_draws,
                total_black_draws,
                Util.player_named_by(total_draws),
                total_white_unfinished,
                total_black_unfinished,
                Util.player_named_by(total_unfinished),
                total_white_games,
                total_black_games,
                Util.player_named_by(total_games)
            ])

        general_stats_table = PrettyTable()
        general_stats_table.field_names = ['TOTAL FILES', 'ERRORS', 'UNKNOW OPPONENT', 'UNDEFINED OPPONENTS']
        general_stats_table.add_row([total_files, total_errors, unknow_opponent, undefined_opponents])

        print(general_stats_table)
        print(leader_board_table)
        print("A B --> (A) [White | Black | Total]; (B) [Wins | Losses | Draws | Unfinished | Games]")

        if opponent is not None:
            print(f"Resume: Jefferson Campos {total_wins} ({total_wins + (total_draws / 2)}) X {total_losses} ({total_losses + (total_draws / 2)}) {opponent}")
            print(tbl_open)
            print(tbl)

    def probability(self, player: float, opponent: float) -> float:
        return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (player - opponent) / 400))

    def elo(self, ra: float, rb: float, k: int = 32) -> Tuple[float, float]:
        pa: float = self.probability(ra, rb)
        pb: float = self.probability(rb, ra)

        ra: float = ra + k * (1 - pa)
        rb: float = rb + k * (0 - pb)

        return (ra, rb)

    def rating(self, choosen: Optional[str] = None, get_infrequents: bool = False) -> None:
        # FIXME not working in universe without other players games. My rating will be 5815.5488...
        ratings: Dict[str, float] = dict()
        games: List = []

        with open(Analysis.DEFAULT_PLAYER_DATA_FILE, encoding="UTF-8") as players_data_file:
            ratings = {f'{player["real_name"]}': PersonalAnaysis.DEFAULT_INITIAL_RATING for player in csv.DictReader(players_data_file, delimiter=";")} if get_infrequents else {f'{player["real_name"]}': PersonalAnaysis.DEFAULT_INITIAL_RATING for player in csv.DictReader(players_data_file, delimiter=";") if player["infrequent"] == "False"}
            # ratings["?"] = PersonalAnaysis.DEFAULT_INITIAL_RATING }

        for path in os.listdir("data/pgn/mgr/"):
            with open("data/pgn/mgr/" + path, encoding="utf-8") as pgn:
                game = chess.pgn.read_game(pgn)

                if choosen is not None:
                    if game.headers["White"] != choosen and game.headers["Black"] != choosen:
                        continue

                if game.headers["White"] == "Jefferson Campos":
                    opponent = game.headers["Black"]
                elif game.headers["Black"] == "Jefferson Campos":
                    opponent = game.headers["White"]
                else:
                    raise Exception(f"Game is not against Jefferson Campos!! {game.headers['White']=} {game.headers['Black']=}")

                if opponent in ratings.keys() and (game.headers["Result"] == "1-0" or game.headers["Result"] == "0-1"):
                    games.append(game)

        og = list(sorted(games, key=lambda x: datetime.strptime(x.headers["Date"], "%Y-%m-%dT%H:%M:%S")))
        for game in og:
            if game.headers["Result"] == "1-0":
                winner = game.headers["White"]
                loser = game.headers["Black"]
            elif game.headers["Result"] == "0-1":
                winner = game.headers["Black"]
                loser = game.headers["White"]
            else:
                continue

            rating_winner = ratings[winner]
            rating_loser = ratings[loser]
            new_rating = self.elo(ra=rating_winner, rb=rating_loser, k=10)
            # breakpoint()
            ratings[winner] = round(new_rating[0], 2)
            ratings[loser] = round(new_rating[1], 2)
            # breakpoint()

        ordered_ratings = OrderedDict(sorted(ratings.items(), key=lambda x: x[1], reverse=True))
        general_stats_table = PrettyTable()
        general_stats_table.field_names = ['#', 'Player', 'Rating']
        for index, (key, value) in enumerate(ordered_ratings.items()):
            general_stats_table.add_row([index + 1, key, value])

        # TODO consider only more than fice games against me and having a little as 0.5 points
        print(general_stats_table)

    def latest_games_perfomance(self, number_games: int = 70, opponent: Optional[str] = None) -> List[str]:
        """See https://ratings.fide.com/calc.phtml - FIDE's site force 70 games (max)"""

        choosen: Optional[str] = None
        games_selected: List[str] = os.listdir("data/pgn/mgr/")
        if opponent is not None and opponent != "Jefferson Campos":
            choosen = opponent
            games_selected = []
            for path in os.listdir("data/pgn/mgr/"):
                with open("data/pgn/mgr/" + path, encoding="utf-8") as pgn:
                    game = chess.pgn.read_game(pgn)
                    if game.headers["White"] != choosen and game.headers["Black"] != choosen:
                        continue

                    games_selected.append(path)

        total_games_selected: int = min(len(games_selected), number_games)
        games_sorted: List = [f"{path}.pgn" for path in list(sorted([path.replace('.pgn', '') for path in games_selected], key=lambda x: datetime.strptime(x, "%Y-%m-%dT%H-%M-%S"), reverse=True))[0:total_games_selected]]
        print(f"{total_games_selected=} oldest: {games_sorted[total_games_selected - 1]} latest: {games_sorted[0]}")
        self.my_games(opponent=choosen, games_played=games_sorted)

        return games_sorted

    def rating_fluctuation(self, number_games: int = 70, opponent: Optional[str] = None) -> None:
        games_sorted: List[str] = self.latest_games_perfomance(number_games=number_games, opponent=opponent)

        initial_rating: float = 1460.00 if opponent != "Jefferson Campos" else 1400.00
        rating: float = 1460.00 if opponent != "Jefferson Campos" else 1400.00
        for path in games_sorted:
            game_result: GameResult
            with open("data/pgn/mgr/" + path, encoding="utf-8") as pgn:
                game = chess.pgn.read_game(pgn)
                if (game.headers["White"] == opponent and game.headers["Result"] == "1-0") or (game.headers["Black"] == opponent and game.headers["Result"] == "0-1"):
                    rating = round(self.elo(ra=rating, rb=initial_rating, k=5)[0], 2)
                elif (game.headers["White"] == opponent and game.headers["Result"] == "0-1") or (game.headers["Black"] == opponent and game.headers["Result"] == "1-0"):
                    rating = round(self.elo(ra=initial_rating, rb=rating, k=5)[1], 2)

        print("------------------------")
        print(f"{rating=}")

    def define_min_valid_game_for_rating(self, get_infrequents: bool = False) -> Tuple[str, int]:
        # [W, L, D, U]
        relevant_games: Dict[str, List(int, int, int, int)]

        with open(Analysis.DEFAULT_PLAYER_DATA_FILE, encoding="UTF-8") as players_data_file:
            relevant_games = {f'{player["real_name"]}': [0, 0, 0, 0] for player in csv.DictReader(players_data_file, delimiter=";")} if get_infrequents else {f'{player["real_name"]}': [0, 0, 0, 0] for player in csv.DictReader(players_data_file, delimiter=";") if player["infrequent"] == "False"}

        del relevant_games["Jefferson Campos"]

        for path in os.listdir("data/pgn/mgr/"):
            with open("data/pgn/mgr/" + path, encoding="utf-8") as pgn:
                game = chess.pgn.read_game(pgn)

                if game.headers["White"] == "Jefferson Campos":
                    opponent = game.headers["Black"]
                elif game.headers["Black"] == "Jefferson Campos":
                    opponent = game.headers["White"]
                else:
                    raise Exception(f"Game is not against Jefferson Campos!! {game.headers['White']=} {game.headers['Black']=}")

                if opponent not in relevant_games.keys():
                    continue

                if game.headers["Result"] == "*":
                    relevant_games[opponent][3] += 1
                elif game.headers["Result"] == "1/2-1/2" or game.headers["Result"] == "0,5-0,5":
                    relevant_games[opponent][2] += 1
                elif (game.headers["Result"] == "1-0" and game.headers["White"] == "Jefferson Campos") or (game.headers["Result"] == "0-1" and game.headers["Black"] == "Jefferson Campos"):
                    relevant_games[opponent][1] += 1
                elif (game.headers["Result"] == "1-0" and game.headers["Black"] == "Jefferson Campos") or (game.headers["Result"] == "0-1" and game.headers["White"] == "Jefferson Campos"):
                    relevant_games[opponent][0] += 1

        total_games: Dict[str, int] = {f"{key}": sum(value) for key, value in relevant_games.items() if value[0] > 0 or value[2] > 0 or value[3] > 0}

        min_games: Tuple[str, int] = min(total_games.items(), key=lambda x: x[1])
        print(f"{min_games=}")

        general_stats_table = PrettyTable()
        general_stats_table.field_names = ["#", "Player", "Wins", "Losses", "Drawns", "Unfinished", "TOTAL Required by FIDE"]
        for index, (key, value) in enumerate(OrderedDict(sorted(relevant_games.items(), key=lambda x: total_games[x[0]] if x[0] in total_games.keys() else 0, reverse=False)).items()):
            total: int = total_games[key] if key in total_games.keys() else 0
            general_stats_table.add_row([index + 1, key, value[0], value[1], value[2], value[3], total])

        print(general_stats_table)

        return min_games


def debug_game(self, game):
    logging.debug(Util.debug("Game was: {g}".format(g=game)))
    with open("data/pgn/mgr/{g}.pgn".format(g=game), encoding="utf-8") as pgn:
        game = chess.pgn.read_game(pgn)
        print(len(game.errors), game.errors)
        print(game)


def extract_opponent_from_my_games(player="Jefferson Campos"):
    pass

def extract_players_from_championship(championship_data_file="stats.csv"):
    pass
