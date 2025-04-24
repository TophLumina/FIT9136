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


def vacuum_action(vacuum: list, action: str) -> None:
    DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    MOVEMENTS = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

    def turn_left() -> None:
        vacuum[2] = DIRECTIONS[(DIRECTIONS.index(vacuum[2]) - 1) % len(DIRECTIONS)]

    def turn_right() -> None:
        vacuum[2] = DIRECTIONS[(DIRECTIONS.index(vacuum[2]) + 1) % len(DIRECTIONS)]

    def clean() -> None:
        cleaning_space[vacuum[0]][vacuum[1]] = True

    def forward() -> None:
        next_pos = [
            vacuum[0] + MOVEMENTS[DIRECTIONS.index(vacuum[2])][0],
            vacuum[1] + MOVEMENTS[DIRECTIONS.index(vacuum[2])][1],
        ]

        # out of bound
        if not (
            next_pos[0] >= 0
            and next_pos[0] < len(cleaning_space)
            and next_pos[1] >= 0
            and next_pos[1] < len(cleaning_space[next_pos[0]])
        ):
            turn_right()
            return

        # cat encountered
        if obstruction_space[next_pos[0]][next_pos[1]] == "c":
            if not obstruction_space[
                next_pos[0] + MOVEMENTS[DIRECTIONS.index(vacuum[2])][0]
            ][next_pos[1] + MOVEMENTS[DIRECTIONS.index(vacuum[2])][1]]:
                pass

        if not cleaning_space[vacuum[0]][vacuum[1]]:
            cleaning_space[next_pos[0]][next_pos[1]] = False
        vacuum[0], vacuum[1] = next_pos

    COMMANDS = {
        "turn-left": turn_left,
        "turn-right": turn_right,
        "clean": clean,
        "forward": forward,
    }

    COMMANDS[action]()


def perform_cleaning(instructions: str, vacuum: list) -> None:
    with open(instructions, "r") as file:
        for line in file:
            vacuum_action(vacuum, line.strip())


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
