from pathlib import Path

TEST_INPUT: str = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


# input = TEST_INPUT.strip().splitlines()
input = Path("puzzle.txt").read_text().splitlines()

splits = []

for line in input:
    print(line)


def find(string, ch):
    return [i for i, ltr in enumerate(string) if ltr == ch]


def replace_str_index(text, index, replacement):
    return '%s%s%s'%(text[:index], replacement, text[index+1:])


split_counter = 0

for line in input:
    # start position
    if "S" in line:
        splits.append([line.index("S")])

    # splitter line
    elif "^" in line:
        new_splits = splits[-1][:]
        splitter_is = find(line, "^")
        # if splitter in line with previous
        for splitter_i in splitter_is:
            if splitter_i in splits[-1]:
                new_splits.pop(new_splits.index(splitter_i))
                new_splits.append(splitter_i - 1)
                new_splits.append(splitter_i + 1)

                split_counter += 1

        splits.append(list(set(new_splits)))

print()

for i, line in enumerate(input):
    # print(line)
    split = splits[i//2]
    new_line = line[:]
    for splitter_i in split:
        new_line = replace_str_index(new_line, splitter_i, "|")
    print(new_line)


print(f"tachyon beam split {split_counter} times")

# part II time lines (all paths)
# from queue import Queue
# paths = []
# q = Queue()
# max_depth = len(splits)
#
# q.put(splits[0])
#
# while not q.empty():
#     v = q.get()
#     if len(v) == max_depth:
#         paths.append(v)
#     else:
#         i = len(v)
#         for s in splits[len(v)]:
#             if abs(v[-1] - s) <= 1:
#                 new_v = v + [s]
#                 q.put(new_v)
#

# part II timelines: count distinct histories (not paths) through the manifold
rows, cols = len(input), len(input[0])

start_row = 0
start_col = input[0].index("S")

# ways[r][c] = number of histories reaching (r, c)
ways = [[0] * cols for _ in range(rows)]
ways[start_row][start_col] = 1

for row in range(start_row, rows - 1):
    for col in range(cols):
        count = ways[row][col]
        if count == 0:
            continue

        cell_below = input[row + 1][col]
        if cell_below == "^":
            if col - 1 >= 0:
                ways[row + 1][col - 1] += count
            if col + 1 < cols:
                ways[row + 1][col + 1] += count
        else:
            ways[row + 1][col] += count

total_timelines = sum(ways[rows - 1])
print(f"quantum timelines: {total_timelines}")




