from pathlib import Path
from io import StringIO
import pandas as pd
import numpy as np

TEST_INPUT: StringIO = StringIO(
    """
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
)

INPUT = "puzzle.txt"

# input = TEST_INPUT
input = INPUT

df = pd.read_csv(input, sep="\s+", header=None, engine="python")

op = {"*": "prod", "+": "sum"}

result = sum(
    [
        getattr(df[col].values[:-1].astype(int), op[df[col].values[-1]])()
        for col in df.columns
    ]
)

print(f"result {result}")

# transpose
# input.seek(0)
# s = input.read()
s = Path(INPUT).open().read()
g1 = [[l for l in line] for line in s.splitlines() if line]
nrows = len(g1)
ncols = max([len(l) for l in g1])
g2 = [[" " for _ in range(nrows)] for _ in range(ncols)]
for r in range(ncols):
    for c in range(ncols):
        try:
            g2[c][r] = g1[r][c]
        except IndexError:
            continue

g2 = np.array(g2)

op_queue = []
digits = []
for row in g2[:, :-1]:
    if (row == " ").all():
        op_queue.append(digits)
        digits = []
    else:
        num = int("".join(row).strip())
        digits.append(num)
else:
    op_queue.append(digits)

result_ii = sum(
    [
        getattr(np.array(q), op[op_val])()
        for q, op_val in zip(op_queue, filter(lambda x: x != " ", g2[:, -1]))
    ]
)

print(f"result ii: {result_ii}")
