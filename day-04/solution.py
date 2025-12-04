from pathlib import Path

TEST_INPUT: str = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip().splitlines()

INPUT: str = Path("puzzle.txt").read_text().strip().splitlines()

# TESTING
input = TEST_INPUT
solution = 13

input = INPUT


def print_grid(grid):
    for line in grid:
        print(line)


def get_neighbours(grid, row, col):
    n_rows = len(grid)
    n_cols = len(grid[0])

    # init
    top_lft, top_mid, top_rgt = None, None, None
    mid_lft, value, mid_rgt = None, None, None
    bot_lft, bot_mid, bot_rgt = None, None, None

    # out of bounds
    oob = " "

    # first row
    if row == 0:
        top_lft = oob
        top_mid = oob
        top_rgt = oob
    # last row
    elif row == n_rows - 1:
        bot_lft = oob
        bot_mid = oob
        bot_rgt = oob

    # first col
    if col == 0:
        top_lft = oob
        mid_lft = oob
        bot_lft = oob
    # last col
    elif col == n_cols -1:
        top_rgt = oob
        mid_rgt = oob
        bot_rgt = oob

    if top_lft is not oob:
        top_lft = grid[row - 1][col - 1]
    if top_mid is not oob:
        top_mid = grid[row - 1][col]
    if top_rgt is not oob:
        top_rgt = grid[row - 1][col + 1]
    if mid_lft is not oob:
        mid_lft = grid[row][col - 1]
    if mid_rgt is not oob:
        mid_rgt = grid[row][col + 1]
    if bot_lft is not oob:
        bot_lft = grid[row + 1][col - 1]
    if bot_mid is not oob:
        bot_mid = grid[row + 1][col]
    if bot_rgt is not oob:
        bot_rgt = grid[row + 1][col + 1]

    value = grid[row][col]

    if value == "@":
        print(top_lft, top_mid, top_rgt)
        print(mid_lft, value, mid_rgt)
        print(bot_lft, bot_mid, bot_rgt)

    return [
        [top_lft, top_mid, top_rgt],
        [mid_lft, value, mid_rgt],
        [bot_lft, bot_mid, bot_rgt]
    ]


def is_accessible(grid, row, col) -> bool:
    max_neighbour_rolls = 4
    nbors = get_neighbours(grid, row, col)

    # is a roll
    if nbors[1][1] == "@":
        # count nbor rolls
        roll_count = sum([1 for nbor_row in nbors for roll in nbor_row if roll == "@"])
        # not including the center roll
        roll_count -= 1

        return roll_count < max_neighbour_rolls

    else:
        # raise ValueError("not a roll")
        return False

    return False


def solution_1(grid):
    accessible_rolls_count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):

            if is_accessible(grid, row, col):
                accessible_rolls_count += 1

    return accessible_rolls_count


def remove_rolls(grid):

    def replace_str_index(text, index, replacement):
        return '%s%s%s'%(text[:index], replacement, text[index+1:])


    replace_count = 0
    new_grid = grid.copy()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if is_accessible(grid, row, col):
                new_grid[row] = replace_str_index(new_grid[row], col, ".")
                replace_count += 1
    return new_grid, replace_count


def solution_2(grid):
    total_replace_count = 0
    while True:
        new_grid, replace_count = remove_rolls(grid)
        total_replace_count += replace_count

        print_grid(new_grid)
        grid = new_grid.copy()
        if replace_count == 0:
            break
    return total_replace_count


if __name__ == "__main__":

    # print_grid(input)
    # print()

    result = solution_1(TEST_INPUT)
    assert result == solution
    print(f"Result solution 1: {result}")

    # print(input)
    # part_1_result = solution_1(input)
    # print(f"Result part I solution 1: {part_1_result}")

    result = solution_2(TEST_INPUT)
    print(f"Result solution 2: {result}")
    assert result == 43

    print(input)
    part_2_result = solution_2(input)
    print(f"Result solution 2: {part_2_result}")
