TEST_INPUT = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".strip().splitlines()

input = TEST_INPUT


def parse_input(input_lines):
    presents = {}
    regions = {}
    final = False
    key = None
    for line in input_lines:
        if ":" in line and "x" not in line:
            key = int(line.strip(":"))
            presents[key] = []
        elif "#" in line or "." in line:
            presents[key].append(line)
        elif line == "":
            final = True
            key = None
        elif "x" in line:
            rkey, values = line.split(":")
            rvalues = [int(val) for val in values.split(" ") if val]
            if rkey in regions:
                regions[rkey].append(rvalues)
            else:
                regions[rkey] = [rvalues]

    return presents, regions


presents, regions = parse_input(input)

print(presents)
print(regions)


def pprint(present):
    print()
    print(f"{len(present)} x {len(present[0])} present")
    for row in present:
        for cell in row:
            print(cell, end=" ")
        print()


def rotate(present):
    """rotate clockwise"""
    nrows, ncols = len(present), len(present[0])

    rpres = [['', '', ''] for _ in range(ncols)]

    # R =
    # [[0, -1],
    #  [1, 0]]

    for y in range(ncols):
        for x in range(nrows):
            pres = present[y][x]

            x -= 1
            y -= 1

            xx = (0 * x) + (-1 * y)
            yy = (1 * x) + (0 * y)

            xx += 1
            yy += 1

            xx %= nrows
            yy %= ncols

            # print(f"({x}, {y}): {pres} -> ({xx}. {yy})", end=" | ")

            rpres[yy][xx] = pres
        # print()
    return rpres


def flip(present):
    nrows, ncols = len(present), len(present[0])

    rpres = [['', '', ''] for _ in range(ncols)]

    for y in range(ncols):
        for x in range(nrows):
            pres = present[y][x]

            xx = x
            yy = (ncols - y)

            rpres[yy][xx] = pres

    return rpres

# present = [
#     [0, 1, 2],
#     [3, 4, 5],
#     [6, 7, 8]
# ]
#
# pprint(present)
# rpres = rotate(present)
# # print(rpres)
# pprint(rpres)



for present in presents.values():
    pprint(present)
    rpres = rotate(present)
    # print(rpres)
    pprint(rpres)

    fpres = flip(present)
    pprint(fpres)
    print("*******")
