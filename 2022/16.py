import math
import re
from functools import cache


lines = list(filter(None, map(lambda x: x.strip(), open("16.txt", "r").readlines())))

pattern = re.compile(
    r"Valve (\S+) has flow rate=(\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)"
)

nodes = [
    (name, int(flow), neighbours.split(", "))
    for name, flow, neighbours in (pattern.match(line).groups() for line in lines)
]
nodes = sorted(nodes)
name2idx = {name: idx for idx, (name, _, _) in enumerate(nodes)}


def floyd_warshall():
    adjacency = [[math.inf] * len(nodes) for _ in range(len(nodes))]
    for idx in range(len(nodes)):
        adjacency[idx][idx] = 0
        for n_idx in map(lambda x: name2idx[x], nodes[idx][2]):
            adjacency[idx][n_idx] = 1
    for k in range(len(nodes)):
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                adjacency[i][j] = min(
                    adjacency[i][j], adjacency[i][k] + adjacency[k][j]
                )

    return adjacency


DISTANCES = floyd_warshall()
assert name2idx["AA"] == 0
assert nodes[0][1] == 0, "AA required to have no valve"
FLOW_RATES = [flow for _, flow, _ in nodes if flow > 0]
assert all(
    v < math.inf for r in DISTANCES for v in r
), "Graph if expected to be fully connected"
POI = tuple(idx for idx, (name, flow, _) in enumerate(nodes) if flow > 0)


@cache
def longest_path(open_set, last, time) -> int:
    total = 0
    for p in open_set:
        t = time - DISTANCES[last][p] - 1
        if t > 0:
            contribution = t * nodes[p][1]
            total = max(total, contribution + longest_path(open_set - {p}, p, t))
    return total


# part 1
print(longest_path(frozenset(POI), 0, 30))


def split_powerset(s):
    x = len(s)
    total = (1 << x) - 1
    for i in range(1 << (x - 1)):
        complement = total - i
        set_a = tuple(s[j] for j in range(x) if (i & (1 << j)))
        set_b = tuple(s[j] for j in range(x) if (complement & (1 << j)))
        yield set_a, set_b


#
# part 2
print(
    max(
        longest_path(frozenset(a), 0, 26) + longest_path(frozenset(b), 0, 26)
        for a, b in split_powerset(POI)
    )
)
