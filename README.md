# Chess #

My study and games played.

# Standards #

## PGN ##

[Standard: Portable Game Notation Specification and Implementation Guide](http://www.tim-mann.org/Standard "HTML")

[Standard: Portable Game Notation Specification and Implementation Guide](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm "TEXT")

## FEN ##

[Standard: Forsyth–Edwards Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation "Wikipedia")

# Data Layout #

I was using layout that is recomended in PGN standard. There is some adaptations:

* All my  games will be stored in _data/pgn/mgr;
* All other players will be stored in _data/pgn/players;
* All filenames will be a timestamp;
** If a game was played at Santa Rosália Bakery and the times is unknow then time will be set at 19:00:00;
** Exercise and other cases, the unknow time will be set to 00:00:00;

# Projects References #

## Good Ideas ##

Rafael Vicente Leite:
* https://github.com/rafaelvleite/freedomChessChromeExtension
* https://github.com/rafaelvleite/centipawn_loss_calculator
* https://github.com/rafaelvleite/speechChess
* https://github.com/rafaelvleite/fide_crawler

## Libs ##

[Python-Chess](https://python-chess.readthedocs.io/en/latest/pgn.html)
[Openingtree](https://www.openingtree.com/)
[BChess](https://github.com/PadawanBreslau/bchess)

# My Analysis #

analysis.debug_game(args.debug_game)



analysis.padoca_championship(championship_data_file="padoca_cup_2022.csv", set_unfinished_column=False)
"""Serve para analisar um campeonato. Pode ser replicado para outros? - campeonato de pontos corridos - todos contra todos"""
clear; date; time python3 jeffchess/main.py -s "padoca-2022-02"; date


analysis.games_by_player(args.games_by_player)
"""Serve para mostrar o resultado de um jogador no campeonato"""
clear; date; time python3 jeffchess/main.py -gbp 'Emerson Sbrana'; date


Ambos vão usar uma lista padrão de campeonato (championship.csv)

analysis.generate_pairing_tables()
"""Combine a list of players to generate a table game"""
clear; date; time python3 jeffchess/main.py -s "pairing"; date


vai usar players.csv

------------------------------

analysis.my_games()
"""Analisa os meus jogos toda a vida"""
clear; date; time python3 jeffchess/main.py -s jeff; date

analysis.generate_list_my_games(args.my_games_opponent)
"""Lista os meus jogos contra um oponente com um destaque para os jogos em aberto."""
clear; date; time python3 jeffchess/main.py -mgo 'João Carlos Oliveira'; date

