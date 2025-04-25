cleaning_space = [
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, False, True, True, True, True, True, True, True],
    #          ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, False, True, True, False, True, True, True, True],
    #          ^^^^^            ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, False, True, True, True, True, True],
    #                     ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
]

obstruction_space = [
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, "c", None, None, None, None, None],
    [None, None, "r", None, None, None, None, None, None, None],
    [None, None, None, None, None, None, "w", None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, "w", None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
]


def vacuum_action(vacuum: list, action: str) -> str:
    DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    MOVEMENTS = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

    def in_area(x: int, y: int) -> bool:
        return (
            y < len(cleaning_space) and y >= 0 and x < len(cleaning_space[y]) and x >= 0
        )

    def _next_pos(x: int, y: int, dir: list) -> list:
        return [y + dir[0], x + dir[1]]

    def turn_left() -> str:
        vacuum[2] = DIRECTIONS[(DIRECTIONS.index(vacuum[2]) - 1) % len(DIRECTIONS)]
        return "turn-left"

    def turn_right() -> str:
        vacuum[2] = DIRECTIONS[(DIRECTIONS.index(vacuum[2]) + 1) % len(DIRECTIONS)]
        return "turn-right"

    def clean() -> str:
        cleaning_space[vacuum[0]][vacuum[1]] = True
        return "clean"

    def forward() -> str:
        next_pos = _next_pos(
            vacuum[1], vacuum[0], MOVEMENTS[DIRECTIONS.index(vacuum[2])]
        )

        # out of bound
        if not in_area(next_pos[1], next_pos[0]):
            return turn_right()

        # cat encountered
        if obstruction_space[next_pos[0]][next_pos[1]] == "c":
            next_pos_cat = _next_pos(
                next_pos[1], next_pos[0], MOVEMENTS[DIRECTIONS.index(vacuum[2])]
            )
            # any obstruction in the cat's next_pos and is the cat still in the obstruction space?
            if not obstruction_space[next_pos_cat[0]][next_pos_cat[1]] and in_area(
                next_pos_cat[1], next_pos_cat[0]
            ):
                obstruction_space[next_pos_cat[0]][next_pos_cat[1]] = "c"
                obstruction_space[next_pos[0]][next_pos[1]] = None

            return turn_right()

        # wall encountered
        if obstruction_space[next_pos[0]][next_pos[1]] == "w":
            return turn_right()

        if not cleaning_space[vacuum[0]][vacuum[1]]:
            cleaning_space[next_pos[0]][next_pos[1]] = False

        # obstruction status update
        obstruction_space[vacuum[0]][vacuum[1]] = None
        obstruction_space[next_pos[0]][next_pos[1]] = "r"

        vacuum[0], vacuum[1] = next_pos

        return "forward"

    COMMANDS = {
        "turn-left": turn_left,
        "turn-right": turn_right,
        "clean": clean,
        "forward": forward,
    }

    return COMMANDS[action]()


def perform_cleaning(instructions: str, vacuum: list, log: str) -> None:
    with open(instructions, "r") as in_file:
        with open(log, "w") as out_file:
            for line in in_file:
                action = vacuum_action(vacuum, line.strip())
                out_file.write(action + "\n")


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    test_commands = "test_commands.txt"
    test_log = "test_log.txt"
    vacuum = [2, 2, "N"]

    print("INITIAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end="")
            elif cell:
                print(".", end="")
            else:
                print("d", end="")
        print()

    print("CLEANING")
    perform_cleaning(test_commands, vacuum, test_log)

    print("FINAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end="")
            elif cell:
                print(".", end="")
            else:
                print("d", end="")
        print()

    print("ACTIONS")
    with open(test_log, "r") as log:
        print(log.read())
