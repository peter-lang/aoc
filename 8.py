from itertools import cycle
from functools import reduce
from math import gcd

lines = list(filter(None, map(lambda x: x.strip(), open("8.txt", "r").readlines())))

INSTRUCTIONS = lines[0]
nodes_by_names = [
    (node, tuple(map(lambda x: x.strip(), children[1:-1].split(","))))
    for node, children
    in (map(lambda x: x.strip(), l.split("=")) for l in lines[1:])
]
idx2node = [n for n, _ in nodes_by_names]
node2idx = {n: idx for idx, n in enumerate(idx2node)}

edges = {node2idx[n]: (node2idx[l], node2idx[r]) for (n, (l, r)) in nodes_by_names}

LEFT_EDGE_TO = [
    edges[i][0]
    for i in range(len(idx2node))
]

RIGHT_EDGE_TO = [
    edges[i][1]
    for i in range(len(idx2node))
]


def path_length_to(start, instruction, end):
    length = 0
    ins_iter = iter(cycle(instruction))
    node = start
    while True:
        ins = next(ins_iter)
        if ins == 'L':
            node = LEFT_EDGE_TO[node]
        elif ins == 'R':
            node = RIGHT_EDGE_TO[node]
        length += 1
        # we need a do-while loop, when we check end-to-end cycles
        if node in end:
            break
    return length, node


# print 1
print(path_length_to(node2idx['AAA'], INSTRUCTIONS, {node2idx['ZZZ']})[0])

# print 2
sources = [idx for idx, name in enumerate(idx2node) if name.endswith('A')]
destinations = set([idx for idx, name in enumerate(idx2node) if name.endswith('Z')])
moduli = []
for src in sources:
    offset_len, dst1 = path_length_to(src, INSTRUCTIONS, destinations)
    cycle_len, dst2 = path_length_to(dst1, INSTRUCTIONS, destinations)
    # first we need to check what are our cycles
    # fortunately, every starting point cycles around distinct end points and len(offset) == len(cycle)
    assert dst1 == dst2
    assert offset_len == cycle_len
    moduli.append(offset_len)

print(reduce(lambda a, b: a*b//gcd(a, b), moduli, 1))
