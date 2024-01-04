from collections import deque

lines = filter(None, map(lambda x: x.strip(), open("6.txt", "r").readlines()))
EDGES = dict()
for a, b in map(lambda x: x.split(")"), lines):
    EDGES.setdefault(a, []).append(b)


def reverse_edges(edges):
    result = dict()
    for parent, children in edges.items():
        for ch in children:
            result.setdefault(ch, []).append(parent)
    return result


def union_edges(a, b):
    return {k: a.get(k, []) + b.get(k, []) for k in set(a.keys()) | set(b.keys())}


def total_descendants(edges, root, depth):
    children = edges.get(root, [])
    return len(children) * depth + sum(
        total_descendants(edges, ch, depth + 1) for ch in children
    )


def bfs(edges, src, tar):
    visited = set()
    nodes = deque([(src, 0)])
    while nodes:
        node, dist = nodes.popleft()
        if node == tar:
            return dist
        visited.add(node)
        for child in edges[node]:
            if child not in visited:
                nodes.append((child, dist + 1))
    return None


# part 1
print(total_descendants(EDGES, "COM", 1))

# part 2
REV_EDGES = reverse_edges(EDGES)
assert len(REV_EDGES["YOU"]) == 1
assert len(REV_EDGES["SAN"]) == 1
print(bfs(union_edges(EDGES, REV_EDGES), REV_EDGES["YOU"][0], REV_EDGES["SAN"][0]))
