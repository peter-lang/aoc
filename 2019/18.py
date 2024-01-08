import heapdict
import math
import string
import numpy as np

lines: list[str] = list(
    filter(None, map(lambda x: x.strip(), open("18.txt", "r").readlines()))
)

code_table = ".#" + string.ascii_lowercase + string.ascii_uppercase
codec = {ch: idx for idx, ch in enumerate(code_table)}
BLOCK = codec["#"]

BOARD = np.array(
    [list(map(lambda ch: codec[ch], line.replace("@", "."))) for line in lines]
)
START = next(
    (row, col)
    for row, line in enumerate(lines)
    for col, ch in enumerate(line)
    if ch == "@"
)


def pt_neighbour(pt):
    yield pt[0] - 1, pt[1]
    yield pt[0] + 1, pt[1]
    yield pt[0], pt[1] - 1
    yield pt[0], pt[1] + 1


# (start[0] + d[0], start[1] + d[1])
def quadrant(d):
    board = np.copy(BOARD)
    board[START[0], :] = BLOCK
    board[:, START[1]] = BLOCK
    if d == (-1, -1):  # top-left
        return board[: (START[0] + 1), : (START[1] + 1)], (START[0] - 1, START[1] - 1)
    if d == (-1, 1):  # top-right
        return board[: (START[0] + 1), START[1] :], (START[0] - 1, 1)
    if d == (1, 1):  # bottom-right
        return board[START[0] :, START[1] :], (1, 1)
    if d == (1, -1):  # bottom-left
        return board[START[0] :, : (START[1] + 1)], (1, START[1] - 1)


def pprint(b):
    for row in b:
        print("".join(code_table[v] for v in row))


# Middle area looks like this:
# ...
# .@.
# ...
# Other than this part, assert that each quadrant would be a tree.
# Quadrants can be solved independently. Transition takes 2 steps between neighbouring quadrant starts.
QUADRANTS = [quadrant(offset) for offset in ((-1, -1), (-1, 1), (1, 1), (1, -1))]


def dfs_dependencies(board, src, parent, visited, doors, dependencies):
    assert src not in visited, "Graph is not a tree"
    visited.add(src)
    val = code_table[board[src]]
    if val.isalpha():
        if val.isupper():
            doors = doors + [val.lower()]
        else:
            dependencies[val] = set(doors)

    for child in pt_neighbour(src):
        if child == parent or board[child] == BLOCK:
            continue
        dfs_dependencies(board, child, src, visited, doors, dependencies)


def all_dependencies():
    result = dict()
    for idx, (quad, quad_src) in enumerate(QUADRANTS):
        dfs_dependencies(quad, quad_src, quad_src, set(), [], result)
    return result


KEY2DEPS = all_dependencies()


def dfs_dists(board, src, parent, edges) -> list[tuple[str, int]]:
    val = code_table[board[src]]

    paths = [
        dfs_dists(board, child, src, edges)
        for child in pt_neighbour(src)
        if child != parent and board[child] != BLOCK
    ]

    # if this is a junction, then pair nodes from each path
    for idx, path_1 in enumerate(paths):
        for path_2 in paths[:idx]:
            for k1, d1 in path_1:
                for k2, d2 in path_2:
                    edges.setdefault(k1, dict())[k2] = d1 + d2 + 2
                    edges.setdefault(k2, dict())[k1] = d1 + d2 + 2
    # increase distance to descendants
    merged = [(k, d + 1) for r in paths for k, d in r]
    # if this is a key node, add it to the result and set its distance to each of its descendants
    if val.isalpha() and val.islower():
        for k, d in merged:
            edges.setdefault(k, dict())[val] = d
            edges.setdefault(val, dict())[k] = d
        merged.append((val, 0))
    return merged


def quad_edges():
    result = [dict() for _ in range(4)]
    for idx, (quad, quad_src) in enumerate(QUADRANTS):
        n = f"@{idx}"
        for k, d in dfs_dists(quad, quad_src, quad_src, result[idx]):
            result[idx].setdefault(n, dict())[k] = d
            result[idx].setdefault(k, dict())[n] = d
    return result


QUAD_EDGES = quad_edges()


def merge_quad_edges():
    result = dict()
    # quadrant sources are all 2 dist from source
    result["@"] = {
        k: v + 2 for i in range(4) for k, v in QUAD_EDGES[i][f"@{i}"].items()
    }

    for idx, edges in enumerate(QUAD_EDGES):
        q_src = f"@{idx}"
        for k1, edge_list in edges.items():
            if k1 != q_src:
                # add every key-pair in quadrant
                k1_merged = {k2: d for k2, d in edge_list.items() if k2 != q_src}
                # for other quadrants, we first go to current quad source
                # transit to other quad source and take every element from there
                d_offset = edge_list[q_src]
                for i in range(4):
                    if i == idx:
                        continue
                    d_trans = 2 if (i - idx) % 2 == 1 else 4
                    for k2, d in QUAD_EDGES[i][f"@{i}"].items():
                        k1_merged[k2] = d_offset + d_trans + d

                k1_merged["@"] = result["@"][k1]
                result[k1] = k1_merged
    return result


MERGED_EDGES = merge_quad_edges()


def update_tuple(prev, i, val):
    return prev[:i] + (val,) + prev[(i + 1) :]


def planning_a_star(srcs, edges, key2deps):
    open_set = heapdict.heapdict()

    for key, deps in key2deps.items():
        if deps:
            continue

        for idx in range(len(edges)):
            if key in edges[idx][srcs[idx]]:
                dict_key = (update_tuple(srcs, idx, key), frozenset({key}))
                dist = edges[idx][srcs[idx]][key]
                open_set[dict_key] = dist

    while open_set:
        node, dist = open_set.popitem()
        srcs, collected = node
        if len(collected) == len(key2deps):
            return dist
        for k2, deps in key2deps.items():
            if k2 in collected or bool(deps - collected):
                continue

            for idx in range(len(edges)):
                if k2 in edges[idx][srcs[idx]]:
                    dict_key = (update_tuple(srcs, idx, k2), collected | {k2})
                    tentative_dist = dist + edges[idx][srcs[idx]][k2]
                    if tentative_dist < open_set.get(dict_key, math.inf):
                        open_set[dict_key] = tentative_dist

    return None


# part 1
print(planning_a_star(("@",), (MERGED_EDGES,), KEY2DEPS))

# part 2
print(planning_a_star(("@0", "@1", "@2", "@3"), QUAD_EDGES, KEY2DEPS))
