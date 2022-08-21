class Player():
    _white = None
    _black = None

    def __init__(self, white, black):
        self._white = white
        self._black = black

    @property
    def white(self):
        return self._white
    @white.setter
    def white(self, value):
        self._white = value
    @white.deleter
    def white(self):
        del self._white

    @property
    def black(self):
        return self._black
    @black.setter
    def black(self, value):
        self._black = value
    @black.deleter
    def black(self):
        del self._black

        # june = {
        #     "name": "Jefferson Campos",
        #     "position": 4,
        #     "white": {
        #         "win": 4,
        #         "draw": 3,
        #         "lost": 2,
        #         "unfinished": 1
        #     },
        #     "black": {
        #         "win": 4,
        #         "draw": 3,
        #         "lost": 2,
        #         "unfinished": 1
        #     },
        #     # FIXME which is better: white: {win, draw, lost, unfinished} (same for black) OR by result as bellow
            
        #     "win": {
        #         "white": 8,
        #         "black": 3
        #     },
        #     "draw": {
        #         "white": 1,
        #         "black": 1
        #     },
        #     "lost": {
        #         "white": 1,
        #         "black": 1,
        #     },
        #     "unfinished": {
        #         "white": 1,
        #         "black": 1
        #     }
        # }
        # # print(june["name"])
        # # print("total games: {t}".format(t = (june["win"]["white"] + june["win"]["black"]) + (june["draw"]["white"] + june["draw"]["black"]) + (june["lost"]["white"] + june["lost"]["black"])))
        # # print("total points: {p}".format(p = (june["win"]["white"] + june["win"]["black"]) + ((june["draw"]["white"] + june["draw"]["black"]) * 0.5) ))

        # # june["name"] = "jeffão"
        # # print(june["name"])
