Your friend Binh is most interested in understanding how others play chess. The explosion of online chess has greatly increased the availability of high-quality gameplay data. The website [lichess.org](http://lichess.org/) is particularly popular, with over 2 TB of chess gameplay data documenting over 6.5 billion rated games.

The games are recorded in the PGN format. A summary of the PGN format can be found here: [https://en.wikipedia.org/wiki/Portable_Game_Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation).

The PGN format consists first of an arbitrary number of blocks of the form, `[tag "information"]`  where a tag consists of alphabetical characters (a-z and A-Z) and the information is a simple string. The blocks are followed by a blank line, with the moves of the game recorded on the following line. The game consists of a set of moves made in rounds. Each round consists of a digit and a period, representing the number of the round, followed by the move made first by white and then by black. An example of a game is given below. The last round may have had no move made by black. The game then ends with a record of who won, `1-0` for white, `0-1`  for black, and `1/2-1/2` for a draw.

```pgn
[Event "Rated Blitz game"]
[Site "https://lichess.org/drdqnvm6"]
[White "german11"]
[Black "ralphhh"]
[Result "0-1"]
[UTCDate "2013.01.06"]
[UTCTime "01:01:07"]
[WhiteElo "1556"]
[BlackElo "1457"]
[WhiteRatingDiff "-14"]
[BlackRatingDiff "+14"]
[ECO "C00"]
[Opening "French Defense: Knight Variation"]
[TimeControl "180+3"]
[Termination "Normal"]

1. e4 e6 2. Nf3 d5 3. exd5 Qxd5 4. d4 Nc6 5. Nc3 Qd7 6. Be3 Nf6 7. Bb5 a6 8. Ba4 b5 9. Bb3 Bd6 10. O-O O-O 11. Bg5 Qe7 12. a3 h6 13. Bh4 g5 14. Bg3 Bxg3 15. fxg3 Bb7 16. Re1 Rad8 17. d5 Nxd5 18. Qe2 Nxc3 19. bxc3 Qf6 20. Rad1 Rxd1 21. Rxd1 Qxc3 22. Nd4 Nxd4 23. Rxd4 Qxd4+ 24. Kh1 Qa1+ 0-1
```


For the sake of this task, all of the games you are given will contain 7 important tags, `Event`, `White`, `Black`, `Result`, `WhiteElo`, `BlackElo`, and `Opening`. A short description of each tag is given below:

* `Event`-The match type or name of the formal event where the game was played.
* `White`-The username of the player using the white pieces.
* `Black`-The username of the player using the black pieces.
* `Result`-The outcome of the game. This matches the last item in the game string.
* `WhiteElo`-The relative strength of the player using the white pieces, or `?` if the player is unrated.
* `BlackElo`-The relative strength of the player using the black pieces, or `?` if the player is unrated.
* `Opening`-The name for the set of initial moves used to start the game.

To help Binh with his analysis, you need to write the 4 functions specified below. You may only import modules that are part of the [Python standard library](https://docs.python.org/3/library/index.html), [pandas](https://pandas.pydata.org/docs/), or [NumPy](https://numpy.org/doc/stable/), as well as Binh's chess functions. To help you with this, Binh has provided you with some sample data files and a scaffold of the 4 functions that Binh wants you to implement.

## Part 1

`def read_pgn(file_name: str) -> list[dict]:` - This function is given a file name and reads the games contained, returning a list of dictionaries containing games. The dictionaries should have the following keys:

```
'event'
'white'
'black'
'result'
'whiteelo'
'blackelo'
'opening'
'w1'
'b1'
'w2'
'b2'
'w3'
'b3'
'w4'
'b4'
'w5'
'b5'
'w6'
'b6'
'w7'
'b7'
'w8'
'b8'
'w9'
'b9'
'w10'
'b10'
'w11'
'b11'
'w12'
'b12'
'w13'
'b13'
'w14'
'b14'
'w15'
'b15'
'w16'
'b16'
'w17'
'b17'
'w18'
'b18'
'w19'
'b19'
'w20'
'b20'
```


The first 7 keys represent the 7 tags that we will require from our games. For each 1⩽i⩽20**1**⩽**i**⩽**20**, `w{i}`, `b{i}` are the moves made by white and black in round `i`, respectively. If white and/or black make no moves in round `i` or the move string is invalid, then the key should have a value of `'-'`. All 20 keys for white and all 20 keys for black are required.

An example of such a dictionary for the earlier game is:

```
{
'event': 'Rated Blitz game',
'white': 'german11',
'black': 'ralphhh',
'result': '0-1',
'whiteelo': '1556',
'blackelo': '1457',
'opening': 'French Defense: Knight Variation',
'w1': 'e4',
'b1': 'e6',
'w2': 'Nf3',
'b2': 'd5',
'w3': 'exd5',
'b3': 'Qxd5',
'w4': 'd4',
'b4': 'Nc6',
'w5': 'Nc3',
'b5': 'Qd7',
'w6': 'Be3',
'b6': 'Nf6',
'w7': 'Bb5',
'b7': 'a6',
'w8': 'Ba4',
'b8': 'b5',
'w9': 'Bb3',
'b9': 'Bd6',
'w10': 'O-O',
'b10': 'O-O',
'w11': 'Bg5',
'b11': 'Qe7',
'w12': 'a3',
'b12': 'h6',
'w13': 'Bh4',
'b13': 'g5',
'w14': 'Bg3',
'b14': 'Bxg3',
'w15'" 'fxg3',
'b15': 'Bb7',
'w16': 'Re1',
'b16': 'Rad8',
'w17': 'd5',
'b17': 'Nxd5',
'w18': 'Qe2',
'b18': 'Nxc3',
'w19': 'bxc3',
'b19': 'Qf6',
'w20': 'Rad1',
'b20': 'Rxd1' 
}
```


## Part 2

Binh would like to see how openings compare. The function `def win_loss_by_opening(games: list[dict]) -> dict:` should take as input a list of games in dictionary format, and return a dictionary with a key for each opening in the dataset and for the values a tuple containing the number of games won by white, followed by the number of games won by black. For example, the file `example.pgn` contains nine games that use the opening `'Van't Kruijs Opening'`. Three of these games are a win for white, `1-0`, 6 wins for black, `0-1`. This means that your dictionary should contain a key `'Van't Kruijs Opening'` with the value `(3, 6)`.

## Part 3

Binh is also interested in the relative strength of players. The function `def win_loss_by_elo(games: list[dict], lower: int, upper: int) -> tuple[int, int]:` should take a list of games in dictionary format as input. We also take as input two non-negative numbers that represent the absolute bounds on the difference of the player's ELOs. Let variables we**w**e and be**b**e represent the white players' elo score and black players' elo score, respectively. For games in which the difference in player strength falls within the range lower<∣we−be∣<upper**l**o**w**er**<**∣**w**e**−**b**e**∣**<**u**pp**er, this function returns a tuple containing the number of games that were won by the player with the lower ELO in the first position, and the number of games that were won by the player with the higher ELO in the second position. For example, the following statements should evaluate to true when run on the file `lichess_small.pgn`:

```python
win_loss_by_elo(data, 0, 600) == (99, 218)
win_loss_by_elo(data, 0, 400) == (98, 197)
win_loss_by_elo(data, 0, 200) == (85, 133)
win_loss_by_elo(data, 0, 100) == (53, 72)
win_loss_by_elo(data, 400, 600) == (1, 21)
```

## Part 4

Lastly, Binh is interested in a program that would allow him to enter a list of moves and find out if the position is better for white or black. The function `def win_loss_by_moves(games: list[dict], moves: list[str]) -> tuple[int, int]:` should take the list of games in dictionary form and a list of moves. The list of moves will contain the white and black moves from the beginning of the game, in an alternating fashion, and will return a tuple of the number of games won by white, followed by the number of games won by black. For example,  `example.pgn` and the following list of moves `['e4', 'e5', 'Nf3']` should return `(3, 2)`, whereas the list `['e4', 'e5', 'Nf3', 'Nc6']` should return `(2, 2)`
