# Part 1
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


# Part 2
def win_loss_by_opening(games: list[dict]) -> dict:
    opening_stats = {}

    for game in games:
        opening = game["opening"]
        result = game["result"]

        if opening not in opening_stats:
            opening_stats[opening] = [0, 0]  # [white, black]

        if result == "1-0":  # White wins
            opening_stats[opening][0] += 1
        elif result == "0-1":  # Black wins
            opening_stats[opening][1] += 1

    return {opening: tuple(stats) for opening, stats in opening_stats.items()}


# Part 3
def win_loss_by_elo(games: list[dict], lower: int, upper: int) -> tuple[int, int]:
    lower_elo_wins = 0
    higher_elo_wins = 0

    for game in games:
        white_elo = game["whiteelo"]
        black_elo = game["blackelo"]
        result = game["result"]

        # Remove games with unknown ELO ratings
        if white_elo == "?" or black_elo == "?":
            continue

        try:
            we = int(white_elo)
            be = int(black_elo)
        except ValueError:
            continue

        elo_diff = abs(we - be)

        if lower < elo_diff < upper:
            if result == "1-0":
                if we < be:
                    lower_elo_wins += 1
                else:
                    higher_elo_wins += 1
            elif result == "0-1":
                if be < we:
                    lower_elo_wins += 1
                else:
                    higher_elo_wins += 1

    return (lower_elo_wins, higher_elo_wins)


# Part 4
def win_loss_by_moves(games: list[dict], moves: list[str]) -> tuple[int, int]:
    white_wins = 0
    black_wins = 0

    for game in games:
        matched_opening_seq = True

        for i, move in enumerate(moves):
            round_num = (i // 2) + 1
            is_white_move = i % 2 == 0

            if round_num > 20:
                matched_opening_seq = False
                break

            if is_white_move:
                game_move = game.get(f"w{round_num}", "-")
            else:
                game_move = game.get(f"b{round_num}", "-")

            if game_move != move:
                matched_opening_seq = False
                break

        if matched_opening_seq:
            result = game["result"]
            if result == "1-0":
                white_wins += 1
            elif result == "0-1":
                black_wins += 1

    return (white_wins, black_wins)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your test code goes here
    games = read_pgn("./Assignment3/task6/example.pgn")
    print("Games read from PGN:" + str(len(games)))
    for game in games:
        print(game)

    opening_stats = win_loss_by_opening(games)
    print("\nWin/loss by opening:")
    for opening, stats in opening_stats.items():
        print(f"{opening}: {stats[0]} wins for White, {stats[1]} wins for Black")

    elo_ranges = [(0, 100), (0, 200), (0, 400), (0, 600), (400, 600)]
    for lower, upper in elo_ranges:
        elo_stats = win_loss_by_elo(games, lower, upper)
        print(
            f"\nELO range {lower}-{upper}: {elo_stats[0]} wins for lower ELO, {elo_stats[1]} wins for higher ELO"
        )

    test_sequences = [["e4", "e5", "Nf3"], ["e4", "e5", "Nf3", "Nc6"], ["e3"]]

    for moves in test_sequences:
        move_stats = win_loss_by_moves(games, moves)
        print(
            f"\nMoves sequence {moves}: {move_stats[0]} wins for White, {move_stats[1]} wins for Black"
        )
