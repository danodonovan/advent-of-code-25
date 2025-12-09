from pathlib import Path
import numpy as np
from itertools import combinations, pairwise

TEST_INPUT = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip().splitlines()

INPUT = Path("puzzle.txt").read_text().splitlines()


# input = TEST_INPUT
input = INPUT

red_tiles = np.array([list(map(int, line.split(","))) for line in input])
max_cols, max_rows = red_tiles.max(axis=0) + [2, 2]
array = np.zeros((max_rows, max_cols))


def display(array, tiles, other):
    tiles = set([(x, y) for x, y in tiles])
    other = set([(x, y) for x, y in other])
    nrows, ncols = array.shape
    for j, row in enumerate(array):
        for i, cell in enumerate(row):
            if (i, j) in other:
                print('O', end='')
            elif (i, j) in tiles:
                print('#', end='')
            else:
                print('.', end='')
        print("")


if len(input) < 100:
	display(array, tiles=red_tiles, other=[])


# Part I
def _calc_area(a, b):
    a, b = np.array(a), np.array(b)
    return (np.abs(a - b) + np.ones(2, dtype=int)).prod()


area = np.array([
    _calc_area(a, b)
    for a, b in combinations(red_tiles, r=2)
])

check_results = [
    (24, [2, 5], [9, 7]),
    (35, [7, 1], [11, 7]),
    (6, [7, 3], [2, 3]),
    (50, [2, 5], [11, 1]),
]

# for score, a, b in check_results:
#     a, b = np.array(a), np.array(b)
#     check_score = _calc_area(a, b)
#     print(score, a, b, " ... ", check_score)
#     assert score == check_score
#     print()

print(f"Max area: {area.max()}\n")

# Part II

# update array
char_array = array.astype("str")
char_array[:] = "."

for x, y in red_tiles:
    char_array[y, x] = "#"

for a, b in list(pairwise(red_tiles)) + [[red_tiles[-1], red_tiles[0]]]:
    # print('first: ', a, b)
    if a[0] == b[0]:
        # print('X const ---')
        start, end = sorted([a[1], b[1]])
        for j in range(start + 1, end):
            # print('x', a, b, ' : ', a[0], j)
            char_array[j, a[0]] = "X"
    elif a[1] == b[1]:
        # print('Y const |')
        start, end = sorted([a[0], b[0]])
        for i in range(start + 1, end):
            # print('y', a, b, ' : ', i, a[1])
            char_array[a[1], i] = "X"
    else:
        raise ValueError(f"{a}, {b}")
    # print()

for row in char_array:
    flip = False
    for left_cell, right_cell in pairwise(row):
        print(left_cell, right_cell, end="   ")
        # if
    print()

def char_display(array):
    nrows, ncols = array.shape
    for j, row in enumerate(array):
        for i, cell in enumerate(row):
            print(cell, end='')
        print("")


char_display(char_array)


check_results_ii = [
    (15, [7, 3], [11, 1]),
    (3, [9, 7], [9, 5]),
    (24, [9, 5], [2, 3]),
]


def create_green_tiles(red_tiles):
    green_tiles = set()
    red_set = set([(x, y) for x, y in red_tiles])

    n = len(red_tiles)
    boundary = red_set.copy()

    for i in range(n):
        current = red_tiles[i]
        next_tile = red_tiles[(i + 1) % n]

        edge_tiles = line_between(current, next_tile)
        green_tiles.update(edge_tiles)
        boundary.update(edge_tiles)

    xs = [x for x, y in red_tiles]
    ys = [y for x, y in red_tiles]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    exterior = set()
    queue = [(min_x - 1, min_y - 1)]

    while queue:
        x, y = queue.pop(0)

        if (x, y) in exterior or (x, y) in boundary:
            continue
        if x < min_x - 1 or x > max_x + 1 or y < min_y - 1 or y > max_y + 1:
            continue

        exterior.add((x, y))

        # Add neighbors to explore
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = (x + dx, y + dy)
            if neighbour not in exterior and neighbour not in boundary:
                queue.append(neighbour)

    # Interior green tiles = all interior tiles that aren't red
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in exterior and (x, y) not in red_set:
                green_tiles.add((x, y))

    return green_tiles


def line_between(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    line = set()

    if x1 == x2:  # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            line.add((x1, y))
    elif y1 == y2:  # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            line.add((x, y1))

    return line



def _condition(a, b, red_tiles, green_tiles):
    x1, y1 = a
    x2, y2 = b

    # Both corners must be red tiles
    if a not in red_tiles or b not in red_tiles:
        return False

    # Define rectangle bounds
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)

    # Create set of valid tiles (red or green)
    valid_tiles = red_tiles | green_tiles

    # Check all tiles within rectangle bounds
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in valid_tiles:
                return False

    return True


green_tiles = create_green_tiles(red_tiles)
red_tiles = set([(x, y) for x, y in red_tiles])


for score, a, b in check_results_ii:
    a, b = tuple(a), tuple(b)

    assert _condition(a, b, red_tiles, green_tiles)

    check_score = _calc_area(a, b)
    # print(score, a, b, " ... ", check_score)
    assert score == check_score
    # print()


print()
for a, b in combinations(red_tiles, r=2):
    # a, b = np.array(a), np.array(b)
    a, b = tuple(a), tuple(b)

    inside = _condition(a, b, red_tiles, green_tiles)
    a2 = _calc_area(a, b)
    if inside and a2 == 24:
        display(array, tiles=red_tiles, other=np.vstack([a, b]))
        print(a, b, a2)
        print()


area_ii = np.array([
    _calc_area(a, b)
    for a, b in combinations(red_tiles, r=2)
    if _condition(a, b, red_tiles, green_tiles)
])

print('Max area ii:', area_ii.max())
assert area_ii.max() == 24


