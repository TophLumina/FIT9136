from binh_chess import possible_moves


def read_pgn(file_name: str) -> list[dict]:
    games = []

    with open(file_name, "r") as file:
        content = file.read()

    # Split content into game blocks using double newlines
    game_blocks = content.strip().split("\n\n")

    i = 0
    while i < len(game_blocks):
        # Check if this block contains headers
        if i < len(game_blocks) and game_blocks[i].strip().startswith("["):
            header_block = game_blocks[i]
            moves_block = game_blocks[i + 1] if i + 1 < len(game_blocks) else ""

            game_dict = {}

            # Initialize all move keys with '-'
            for round_num in range(1, 21):
                game_dict[f"w{round_num}"] = "-"
                game_dict[f"b{round_num}"] = "-"

            # Parse header tags using split
            header_lines = header_block.strip().split("\n")
            for line in header_lines:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    tag_content = line[1:-1]
                    tag_parts = tag_content.split(" ", 1)  # Split only on first space
                    if len(tag_parts) == 2:
                        tag = tag_parts[0]
                        value_with_quotes = tag_parts[1].strip()
                        if value_with_quotes.startswith(
                            '"'
                        ) and value_with_quotes.endswith('"'):
                            value = value_with_quotes[1:-1]

                            tag_lower = tag.lower()
                            if tag_lower == "event":
                                game_dict["event"] = value
                            elif tag_lower == "white":
                                game_dict["white"] = value
                            elif tag_lower == "black":
                                game_dict["black"] = value
                            elif tag_lower == "result":
                                game_dict["result"] = value
                            elif tag_lower == "whiteelo":
                                game_dict["whiteelo"] = value
                            elif tag_lower == "blackelo":
                                game_dict["blackelo"] = value
                            elif tag_lower == "opening":
                                game_dict["opening"] = value

            if moves_block.strip():
                moves_str = moves_block.strip()

                # Remove game result
                game_result = ["1-0", "0-1", "1/2-1/2"]
                for result in game_result:
                    if moves_str.endswith(result):
                        moves_str = moves_str[: -len(result)].strip()
                        break

                # Split moves into tokens
                move_tokens = moves_str.split()
                current_round = 1
                expecting_white = True

                for token in move_tokens:
                    token = token.strip()
                    if not token:
                        continue

                    # Check if token is a round number
                    if token.endswith(".") and token[:-1].isdigit():
                        current_round = int(token[:-1])
                        expecting_white = True
                    else:
                        if token not in game_result:
                            if current_round <= 20:
                                if expecting_white:
                                    game_dict[f"w{current_round}"] = token
                                    expecting_white = False
                                else:
                                    game_dict[f"b{current_round}"] = token
                                    current_round += 1
                                    expecting_white = True

            # Check if all required keys are present
            required_keys = [
                "event",
                "white",
                "black",
                "result",
                "whiteelo",
                "blackelo",
                "opening",
            ]
            if all(key in game_dict for key in required_keys):
                games.append(game_dict)

            i += 2  # Skip header and moves blocks
        else:
            i += 1

    return games


# Part 1
def count_positions(moves: list[str], depth: int) -> int:
    if depth == 0:
        return 1  # leaf node

    possible_moves_list = possible_moves(moves)
    possible_positions = 0

    for move in possible_moves_list:
        next_board_state = moves + [move]
        possible_positions += count_positions(next_board_state, depth - 1)

    return possible_positions


# Part 2
def winning_statistics(
    file_name: str, depth: int, tolerance: int
) -> tuple[float, list[str], int]:
    games = read_pgn(file_name)
    return inner_winning_statistics(games, [], depth, tolerance)


def match_sequence(game: dict, seq: list[str]) -> bool:
    """
    Check if the game matches the given sequence of moves.
    """
    for i, move in enumerate(seq):
        round_num = (i // 2) + 1
        is_white_move = i % 2 == 0

        if round_num > 20:
            return False

        if is_white_move:
            game_move = game.get(f"w{round_num}", "-")
        else:
            game_move = game.get(f"b{round_num}", "-")

        if game_move != move:
            return False

    return True


def sequence_statistics(games: list[dict], seq: list[str]) -> tuple[float, int]:
    """
    Calculate the win rate of white for games that match the given sequence.
    """
    white_wins = 0
    total_games = 0

    for game in games:
        if match_sequence(game, seq):
            total_games += 1
            if game["result"] == "1-0":  # White wins
                white_wins += 1

    if total_games == 0:
        return (0, 0)

    win_rate = white_wins / total_games
    return (win_rate, total_games)


def inner_winning_statistics(
    games: list[dict], board_state: list[str], depth: int, tolerance: int
) -> tuple[float, list[str], int]:
    """
    Recursive function to find the best winning sequence of moves.
    """
    # Leaf node condition
    if depth == 0:
        current_win_rate, current_total_games = sequence_statistics(games, board_state)
        if current_total_games >= tolerance:
            return (current_win_rate, board_state, current_total_games)
        else:
            return (0.0, [], 0)

    best_win_rate = 0.0
    best_sequence = []
    best_total_games = 0

    # All possible moves from the current board state
    possible_moves_list = possible_moves(board_state)

    for move in possible_moves_list:
        next_seq = board_state + [move]

        # Recursive call to find the winning statistics for the next move
        recursive_win_rate, recursive_sequence, recursive_total_games = (
            inner_winning_statistics(games, next_seq, depth - 1, tolerance)
        )

        # Update the best sequence if the current one is better
        if recursive_win_rate > best_win_rate:
            best_win_rate = recursive_win_rate
            best_sequence = recursive_sequence
            best_total_games = recursive_total_games

    return (best_win_rate, best_sequence, best_total_games)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    assert count_positions([], 1) == 20
    assert count_positions([], 2) == 400
    assert count_positions([], 3) == 8902
    assert count_positions([], 4) == 197281
    assert (
        count_positions(
            [
                "e4",
                "e6",
                "Nf3",
                "d5",
                "exd5",
                "Qxd5",
                "d4",
                "Nc6",
                "Nc3",
                "Qd7",
                "Be3",
                "Nf6",
            ],
            3,
        )
        == 55707
    )

    assert winning_statistics("./Assignment3/task7/lichess_small.pgn", 3, 5) == (
        1.0,
        ["d4", "d6", "c4"],
        5,
    )
    assert winning_statistics("./Assignment3/task7/lichess_small.pgn", 3, 6) == (
        0.8571428571428571,
        ["d4", "d5", "c4"],
        21,
    )
    assert winning_statistics("./Assignment3/task7/lichess_small.pgn", 3, 22) == (
        0.6585365853658537,
        ["e4", "e5", "Nf3"],
        41,
    )
    assert winning_statistics("./Assignment3/task7/lichess_small.pgn", 3, 42) == (
        0,
        [],
        0,
    )
