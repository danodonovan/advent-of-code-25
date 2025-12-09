from pathlib import Path
import numpy as np
from itertools import combinations

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


input = TEST_INPUT
# input = INPUT

red_tiles = np.array([list(map(int, line.split(","))) for line in input])
max_cols, max_rows = red_tiles.max(axis=0) + [2, 2]
array = np.zeros((max_rows, max_cols))


def display(array, tiles):
    tiles = set([(x, y) for x, y in tiles])
    nrows, ncols = array.shape
    for j, row in enumerate(array):
        for i, cell in enumerate(row):
            if (i, j) in tiles:
                print('#', end='')
            else:
                print('.', end='')
        print("")


if len(input) < 100:
	display(array, tiles=red_tiles)


def _calc_area(a, b):
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


for score, a, b in check_results:
    a, b = np.array(a), np.array(b)
    check_score = _calc_area(a, b)
    print(score, a, b, " ... ", check_score)
    assert score == check_score
    print()

# Part I
print(f"Max area: {area.max()}")
