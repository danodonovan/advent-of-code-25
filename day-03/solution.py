from pathlib import Path
import numpy as np

TEST_INPUT: str = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip().split("\n")

INPUT: str = Path("puzzle.txt").read_text().strip().split("\n")

def _as_array(input):
    return np.array([[int(char) for char in line] for line in input])


def solve_1(input):
    jolts = []
    for bank in input:
        b0_bank = bank[:-1]
        b0_ix = bank[:-1].argmax()
        b1_bank = bank[b0_ix + 1:]
        b1_ix = bank[b0_ix + 1:].argmax()
        jolts.append(int(f"{b0_bank[b0_ix]}{b1_bank[b1_ix]}"))
    print(sum(jolts))


def solve_2(input):
    jolts = []
    for bank in input:
        battery = []
        buffer = len(bank) - 12
        while True:
            if buffer > 0:
                buf_bank = bank[:buffer + 1]
                i = buf_bank.argmax()
                buffer -= i
                bank = bank[i:]
            else:
                i += 1

            battery.append(int(bank[0]))
            bank = bank[1:]

            if len(battery) == 12:
                break
        jolts.append(int(''.join(map(str, battery))))
    print(sum(jolts))


# puzzle_input = _as_array(TEST_INPUT)
puzzle_input = _as_array(INPUT)
# solve_1(puzzle_input)
solve_2(puzzle_input)

