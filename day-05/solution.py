from pathlib import Path
from itertools import pairwise
import numpy as np
from scipy.sparse import lil_array
from tqdm import tqdm

TEST_INPUT: str = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip().split("\n")


INPUT: str = Path("puzzle.txt").read_text().strip().split("\n")


def parse(input):
    fresh_ranges = []
    available_ingredients = []

    fresh_range_flag = True
    for line in input:
        if line == "":
            fresh_range_flag = False
            continue

        if fresh_range_flag:
            fresh_ranges.append(line)
        else:
            available_ingredients.append(line)

    return fresh_ranges, available_ingredients


def find_fresh_ingredients(fresh_ranges):
    fresh_ranges = list(map(lambda line: list(map(int, line.split("-"))), fresh_ranges))
    fresh_ranges = sorted(fresh_ranges, key=lambda _range: _range[0])

    while True:
        new_ranges = []

        for (a_start, a_end), (b_start, b_end) in pairwise(fresh_ranges):
            no_overlaps = True

            if a_end < b_start:
                new_ranges.append([a_start, a_end])
            else:
                no_overlaps = False
                new_ranges.append([min(a_start, b_start), max(a_end, b_end)])

        if no_overlaps:
            break
        else:
            fresh_ranges = new_ranges.copy()

    return fresh_ranges


def sum_fresh(fresh_ingredients_ranged, available_ingredients):
    ingredients = set(map(int, available_ingredients))

    result = set([
        ingredient
        for fr_start, fr_stop in fresh_ingredient_ranges
        for ingredient in ingredients
        if fr_start <= ingredient <= fr_stop
    ])

    return len(result)



if __name__ == "__main__":
    # test result should be 3
    # input = TEST_INPUT
    # part 1 result should be 865
    input = INPUT

    fresh_ranges, available_ingredients = parse(input)
    print(
        f"input parsed: {len(fresh_ranges)} fresh ranges, "
        f"{len(available_ingredients)} available ingredients"
    )

    fresh_ingredient_ranges = find_fresh_ingredients(fresh_ranges)
    print(f"found {len(fresh_ingredient_ranges)} fresh ingredient ranges")

    sum_fresh = sum_fresh(fresh_ingredient_ranges, available_ingredients)
    print(f"{sum_fresh} available ingredients are fresh")
