from pathlib import Path
from collections import deque
import itertools

TEST_INPUT = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip().splitlines()

INPUT = Path("puzzle.txt").read_text().strip().splitlines()

# input = TEST_INPUT
input = INPUT

start_node = "you"
end_node = "out"


def parse_input(input):
    graph = {}
    for line in input:
        node, edges = line.split(": ")
        assert node not in graph
        graph[node] = set(edges.split(" "))
    return graph


graph = parse_input(input)


def flatten(container):
    for i in container:
        if isinstance(i, list) and isinstance(i[0], str):
            for j in flatten(i):
                yield j
        else:
            yield i


def find_paths(graph, start, end):

    def _find_paths(graph, start, end, path):
        path = path + [start]
        if start == end:
            return [path]
        return [
            _find_paths(graph, node, end, path)
            for node in graph[start] - set(path)
        ]

    return flatten(_find_paths(graph, start, end, []))


paths = find_paths(graph, start_node, end_node)


print(f"solution: {len(list(paths))}")


TEST_INPUT_II = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip().splitlines()

# input_ii = TEST_INPUT_II
input_ii = INPUT

start_node = "svr"
end_node = "out"
graph_ii = parse_input(input_ii)

## this is combinatorially too expensive
# paths_ii = [
#     path
#     for path in find_paths(graph_ii, start_node, end_node)
#     if "dac" in path and "fft" in path
# ]
# print(f"solution ii: {len(paths_ii)}")

def count_paths_with_required_nodes(graph, start, end, required_nodes):
    required_set = frozenset(required_nodes)
    memo = {}

    def _count(node, visited_required):
        if node == end:
            return 1 if visited_required == required_set else 0

        key = (node, visited_required)
        if key in memo:
            return memo[key]

        if node in required_set:
            new_visited = visited_required | {node}
        else:
            new_visited = visited_required

        count = sum(_count(neighbor, new_visited) for neighbor in graph.get(node, set()))
        memo[key] = count
        return count

    return _count(start, frozenset())


count = count_paths_with_required_nodes(graph_ii, "svr", "out", ["dac", "fft"])

print(f"solution ii: {count}")

