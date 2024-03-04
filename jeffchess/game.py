from enum import Enum
import logging

from util import Util


class ResultType(Enum):
    WIN: str = '1-0'
    LOSS: str = ''
    DRAWN: str = ''
    UNFINISHED: str = '*'


class ResultValue(Enum):
    WIN: float = 1.0
    LOSS: float = 0.0
    DRAWN: float = 0.5
    UNFINISHED: float = 0.0


class GameResult():
    _target_player = "Jefferson Campos"
    _timestamp = None
    _white = None
    _black = None
    _result = None
    _filename = None

    def __init__(self, timestamp, white, black, result, filename, target_player="Jefferson Campos"):
        self._timestamp = timestamp
        self._white = white
        self._black = black
        self._result = result
        self._filename = filename
        self._target_player = target_player

    def target_player_result(self, tp):
        if tp is None:
            tp = self._target_player

        color_target_player = None
        result = None

        if (self._white == self._target_player):
            color_target_player = "White"
        elif (self._black == self._target_player):
            color_target_player = "Black"
        else:
            raise Exception("Target Player not found!")

        if (self._result == "1-0" and self._white == self._target_player) or (self._result == "0-1" and self._black == self._target_player):
            result = "wins"
        elif (self._result == "1-0" and self._black == self._target_player) or (self._result == "0-1" and self._white == self._target_player):
            result = "losses"
        elif self._result == "0,5-0,5" or self._result == "1/2-1/2":
            result = "draws"
        elif self._result == "*":
            result = "unfinished"
        else:
            logging.error(Util.error("result: {r}".format(r=self._result)))
            logging.error(Util.error("timestamp: {t}".format(t=self._timestamp)))
            logging.error(Util.error("white: {w}".format(w=self._white)))
            logging.error(Util.error("black: {b}".format(b=self._black)))
            logging.error(Util.error("target_player: {tp}".format(tp=self._target_player)))
            raise Exception("Invalid Result!!")

        return color_target_player, result

    def opponent_color(self):
        oc = None
        if self._white == self._target_player:
            oc = "Black"
        elif self._black == self._target_player:
            oc = "White"
        else:
            logging.error(Util.error("result: {r}".format(r=self._result)))
            logging.error(Util.error("timestamp: {t}".format(t=self._timestamp)))
            logging.error(Util.error("white: {w}".format(w=self._white)))
            logging.error(Util.error("black: {b}".format(b=self._black)))
            logging.error(Util.error("target_player: {tp}".format(tp=self._target_player)))
            raise Exception("Target player not found! Unable to identify opponent's color!")

        return oc

    def is_against(self, opponent):
        it_is = False
        if self._white == opponent or self._black == opponent:
            it_is = True

        return it_is

    def is_undefined_game(self):
        return True if (self._white == "?" and self._black == "?") else False

    def points(self):
        result = None
        point = None
        if self._result == "1-0":
            result = "White"
            point = 1
        elif self._result == "0-1":
            result = "Black"
            point = 1
        elif self._result == "0,5-0,5" or self._result == "1/2-1/2":
            result = "Draw"
            point = 0.5
        elif self._result == "*":
            result = "unfinished"
            point = 0
        else:
            raise Exception("Invalid Result!!")

        return result, point

    def has_winnwer(self) -> bool:
        has_winner: bool = False

        if self._result == "1-0" or self._result == "0-1":
            has_winner = True

        return has_winner
