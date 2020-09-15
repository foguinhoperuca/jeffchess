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

## Libs ##

[Python-Chess](https://python-chess.readthedocs.io/en/latest/pgn.html)
[Openingtree](https://www.openingtree.com/)
