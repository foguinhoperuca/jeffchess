import logging
from util import Util

class OpponentStats():
    def __init__(self, name):
        self._name = name
        self._white = {
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "unfinished": 0
        }
        self._black = {
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "unfinished": 0
        }

    @property
    def name(self):
        return self._name

    @property
    def white(self):
        return self._white

    @property
    def black(self):
        return self._black

    # TODO count monthly stats
    def count_result(self, game):
        color, result_type = game.target_player_result("Jefferson Campos")
        logging.debug(Util.debug("color: {c}, result_type: {r}".format(c = color, r = result_type)))
        
        if color == "White":
            self._white[result_type] += 1
        elif color == "Black":
            self._black[result_type] += 1
        else:
            raise Exception("Invalid Color!!")
