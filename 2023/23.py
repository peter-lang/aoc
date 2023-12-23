from typing import Iterator
import math

board = list(filter(None, map(lambda x: x.strip(), open("23.txt", "r").readlines())))

MAX_ROW = len(board)
MAX_COL = len(board[0])
START = (0, 1)
END = (MAX_ROW - 1, MAX_COL - 2)

NODE = tuple[int, int]


def neighbours(n) -> Iterator[NODE]:
    if n[0] > 0:
        yield n[0] - 1, n[1]
    if n[0] < MAX_ROW - 1:
        yield n[0] + 1, n[1]
    if n[1] > 0:
        yield n[0], n[1] - 1
    if n[1] < MAX_COL - 1:
        yield n[0], n[1] + 1


def slope_valid(p: NODE, ch: NODE) -> bool:
    if board[p[0]][p[1]] == "<":
        return ch == (p[0], p[1] - 1)
    elif board[p[0]][p[1]] == ">":
        return ch == (p[0], p[1] + 1)
    elif board[p[0]][p[1]] == "v":
        return ch == (p[0] + 1, p[1])
    elif board[p[0]][p[1]] == "^":
        return ch == (p[0] - 1, p[1])
    else:
        return True


def valid_children(p: NODE, check_slope: bool, prev: NODE | None) -> list[NODE]:
    result = []
    for ch in neighbours(p):
        if (
            board[ch[0]][ch[1]] != "#"
            and (not check_slope or slope_valid(p, ch))
            and (prev is None or ch != prev)
        ):
            result.append(ch)
    return result


def next_nodes(p: NODE, check_slope: bool) -> list[tuple[NODE, int]]:
    result = []
    path_starts = valid_children(p, check_slope, None)
    for path_start in path_starts:
        children = None
        curr, prev, weight = path_start, p, 1
        while (
            curr not in (START, END)
            and len((children := valid_children(curr, check_slope, prev))) == 1
        ):
            curr, prev, weight = children[0], curr, weight + 1
        if curr in (START, END) or children:
            result.append((curr, weight))
    return result


def create_reduced_graph(check_slope: bool) -> dict[NODE, list[tuple[NODE, int]]]:
    open_set = {START}
    result = dict()
    while open_set:
        node = open_set.pop()
        children = next_nodes(node, check_slope)
        result[node] = children
        open_set.update((ch for ch, _ in children if ch not in result))
    return result


def longest_path_from(
    node: NODE, visited: set[NODE], graph: dict[NODE, list[tuple[NODE, int]]]
) -> int:
    if node == END:
        return 0
    return max(
        (
            longest_path_from(child, visited | {node}, graph) + weight
            for child, weight in graph[node]
            if child not in visited
        ),
        default=-math.inf,
    )


print(longest_path_from(START, set(), create_reduced_graph(True)))
print(longest_path_from(START, set(), create_reduced_graph(False)))
