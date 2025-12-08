from itertools import combinations
from pathlib import Path
import numpy as np
import math
import pprint


TEST_INPUT = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip().splitlines()

INPUT = Path("puzzle.txt").read_text().strip().splitlines()

# input = TEST_INPUT
# n_connections = 10
input = INPUT
n_connections = 1000


array = np.array([
    [int(d) for d in row.split(",")]
    for row in input
], dtype=int)

junction_combinations = np.array(list(combinations(array, 2)))
straight_line_dist = np.array([np.linalg.norm(abs(a - b)) for a, b in junction_combinations])

# closest pair
sorted_closest_indices = np.argsort(straight_line_dist)
sorted_closest_junctions = junction_combinations[sorted_closest_indices]

from collections import defaultdict
circuits = defaultdict(set)
rev_circuits = dict()
for i, junction in enumerate(array.tolist()):
    junction = tuple(junction)
    circuits[i].add(junction)
    rev_circuits[junction] = i


for i, (a, b) in enumerate(sorted_closest_junctions, start=1):
    print(i, a, b)
    a, b = tuple(map(int, a)), tuple(map(int, b))

    for circuit, junctions in circuits.items():
        if a in junctions:
            circuit_a = circuit
        if b in junctions:
            circuit_b = circuit

    for junction in circuits[circuit_a] | circuits[circuit_b]:
        rev_circuits[junction] = circuit_a

    circuits = defaultdict(set)
    for junction, circuit in rev_circuits.items():
        circuits[circuit].add(junction)

    if i == n_connections:
        break

# print()
# pprint.pp(circuits)

# print()
# pprint.pp(rev_circuits)

sizes = sorted([len(junctions) for junctions in circuits.values()], reverse=True)
result = math.prod(sizes[:3], start=1)

print(result, sum(sizes))

# part II
circuits = defaultdict(set)
rev_circuits = dict()
for i, junction in enumerate(array.tolist()):
    junction = tuple(junction)
    circuits[i].add(junction)
    rev_circuits[junction] = i


for i, (a, b) in enumerate(sorted_closest_junctions, start=1):
    print(i, a, b)
    a, b = tuple(map(int, a)), tuple(map(int, b))

    for circuit, junctions in circuits.items():
        if a in junctions:
            circuit_a = circuit
        if b in junctions:
            circuit_b = circuit

    for junction in circuits[circuit_a] | circuits[circuit_b]:
        rev_circuits[junction] = circuit_a

    circuits = defaultdict(set)
    for junction, circuit in rev_circuits.items():
        circuits[circuit].add(junction)

    if len(circuits) == 1:
        break

print(f"extension cable length: {a[0] * b[0]}")
