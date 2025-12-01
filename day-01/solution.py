from pathlib import Path

DEBUG_INPUT: str = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".strip().splitlines()

DEBUG_2_INPUT: str = """
R1000
""".strip().splitlines()

TEST_INPUT: str = Path("day-01/input.txt").read_text().strip().splitlines()

def _parse(instruction: str) -> int:
    direction, turns = instruction[0], int(instruction[1:])
    if direction == "L":
        return -1, turns
    elif direction == "R":
        return 1, turns
    else:
        raise ValueError(f"Invalid instruction: {instruction}")


# The dial starts by pointing at 50.
INPUT = TEST_INPUT
dial = 50
dial_zero_position_count: int = 0

## solution part 1
"""
for instruction in INPUT:
    direction, turns = _parse(instruction)

    # rotate the dial
    dial = (dial + (direction * turns)) % 100

    if dial == 0:
        dial_zero_position_count += 1

    print(f"The dial is rotated {instruction} to point at {dial}.")

print(f"total zero position count: {dial_zero_position_count}")
"""

## solution part 2
for instruction in INPUT:
    direction, turns = _parse(instruction)

    # rotate the dial
    for _ in range(turns):
        dial = (dial + direction) % 100

        if dial == 0:
            dial_zero_position_count += 1

    print(f"The dial is rotated {instruction} to point at {dial}.")

print(f"total zero position count: {dial_zero_position_count}")


