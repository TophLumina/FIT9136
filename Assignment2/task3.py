cleaning_space = [
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, False, True, True, True, True, True, True, True],
    #          ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, False, True, True, False, True, True, True, True],
    #          ^^^^^           ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, False, True, True, True, True, True],
    #                    ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
]


def vacuum_action(vacuum: list, action: str) -> None:
    DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    MOVEMENTS = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

    def in_area(x: int, y: int) -> bool:
        return (
            y < len(cleaning_space) and y >= 0 and x < len(cleaning_space[y]) and x >= 0
        )

    def _next_pos(x: int, y: int, dir: list) -> list:
        return [y + dir[0], x + dir[1]]

    def turn_left() -> None:
        vacuum[2] = DIRECTIONS[(DIRECTIONS.index(vacuum[2]) - 1) % len(DIRECTIONS)]

    def turn_right() -> None:
        vacuum[2] = DIRECTIONS[(DIRECTIONS.index(vacuum[2]) + 1) % len(DIRECTIONS)]

    def clean() -> None:
        cleaning_space[vacuum[0]][vacuum[1]] = True

    def forward() -> None:
        next_pos = _next_pos(
            vacuum[1], vacuum[0], MOVEMENTS[DIRECTIONS.index(vacuum[2])]
        )

        # out of bound
        if not in_area(next_pos[1], next_pos[0]):
            turn_right()
            return

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
    vacuum = [2, 2, "N"]

    print("INITIAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) == (vacuum[0], vacuum[1]):
                print("r", end="")
            elif cell:
                print(".", end="")
            else:
                print("d", end="")
        print()

    print("CLEANING")
    perform_cleaning(test_commands, vacuum)

    print("FINAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) == (vacuum[0], vacuum[1]):
                print("r", end="")
            elif cell:
                print(".", end="")
            else:
                print("d", end="")
        print()
