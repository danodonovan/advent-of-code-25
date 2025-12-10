from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

TEST_INPUT = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip().splitlines()

INPUT = Path("puzzle.txt").read_text().strip().splitlines()

input = TEST_INPUT
input = INPUT


def parse_line(line):
    splits = line.split(" ")
    machine = None
    buttons_list_str = []
    joltage = None
    for split in splits:
        if split.startswith("["):
            machine = parse_machine(split)
        elif split.startswith("("):
            buttons_list_str.append(split)
        elif split.startswith("{"):
            joltage = parse_joltage(split)

    buttons = parse_buttons(buttons_list_str)

    return machine, buttons, joltage


def parse_machine(machine_str):
    return np.array(
        list(map(lambda l: False if l == "." else True, machine_str.strip("[]")))
    )


def parse_buttons(buttons_list_str):
    buttons = [eval(b) for b in buttons_list_str]
    return [list(b) if isinstance(b, tuple) else [b] for b in buttons]


def parse_joltage(joltage_str):
    return np.array(list(map(int, joltage_str.strip("{}").split(","))))


def press(machine, button):
    machine[button] ^= True
    return machine


def start_machine(size):
    return np.zeros(size, dtype=np.bool)


def solve(target, buttons):
    final_sequence = None
    n_comb = 1
    while n_comb < 100:
        # print(f'N combinations: {n_comb}')

        for sequence in combinations_with_replacement(buttons, r=n_comb):
            machine = start_machine(len(target))

            for button in sequence:
                machine = press(machine, button)

            # print(sequence)
            # print(machine, target)
            # print()

            if (machine == target).all():
                final_sequence = sequence
                break

        if final_sequence is not None:
            break
        n_comb += 1

    return final_sequence


# count = 0
# for machine, buttons, _ in map(parse_line, input):
#     print(f"solving {machine}")
#     sequence = solve(machine, buttons)
#     print(f"sequence {sequence}")
#     print()
#     count += len(sequence)
#     # break
#
# print(f"final solution {count}")
# print()


def start_jolts(size):
    return np.zeros(size, dtype=np.int32)


def press_jolts(machine, button):
    machine[button] += 1
    return machine


def early_check(jolts, target):
    return np.any(jolts > target)


def solve_jolts(target_jolts, buttons):
    final_sequence = None
    n_comb = 1
    while n_comb < 100:
        # print(f'N combinations: {n_comb}')

        for sequence in combinations_with_replacement(buttons, r=n_comb):
            jolts = start_jolts(len(target_jolts))

            for button in sequence:
                jolts = press_jolts(jolts, button)

                if early_check(jolts, target_jolts):
                    # print(f'  early break {jolts} > {target_jolts}')
                    break

            # print(sequence)
            # print(jolts, target_jolts)
            # print()

            if (jolts == target_jolts).all():
                final_sequence = sequence
                break

        if final_sequence is not None:
            break
        n_comb += 1

    return final_sequence


def solve_jolts_ii(target_jolts, buttons):
    n_buttons = len(buttons)
    n_counters = len(target_jolts)

    # Build constraint matrix A where A[i,j] = 1 if button j affects counter i
    A_eq = np.zeros((n_counters, n_buttons))
    for j, button in enumerate(buttons):
        for counter_idx in button:
            A_eq[counter_idx, j] = 1

    # Objective: minimize sum of all button presses
    c = np.ones(n_buttons)

    # Solve using INTEGER linear programming
    # Create constraints: A_eq @ x == target_jolts
    constraints = LinearConstraint(A_eq, target_jolts, target_jolts)

    # All variables are non-negative integers
    bounds = Bounds(lb=0, ub=np.inf)

    # Use milp for integer programming
    integrality = np.ones(n_buttons)  # All variables must be integers

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    return int(result.fun)  # Total presses


count_jolts = 0
for _, buttons, joltage in map(parse_line, input):
    print(f"solving joltage {joltage}")
    count_jolts += solve_jolts_ii(joltage, buttons)
    print(f"sequence count {count_jolts}")
    print()
    # count_jolts += len(sequence)
    # break

print(f"final joltage solution {count_jolts}")
