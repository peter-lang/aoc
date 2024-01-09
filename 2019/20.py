import numpy as np
from collections import deque
from functools import partial


def parse(lines):
    portal_ch = dict()
    maze = dict()
    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch.isalpha():
                portal_ch[(row, col)] = ch
            elif ch == "#":
                maze[(row, col)] = False
            elif ch == ".":
                maze[(row, col)] = True
    row_min, row_max = min(r for r, c in maze.keys()), max(r for r, c in maze.keys())
    col_min, col_max = min(c for r, c in maze.keys()), max(c for r, c in maze.keys())

    def is_edge(pt):
        return pt[0] in (row_min, row_max) or pt[1] in (col_min, col_max)

    assert row_min == 2 and col_min == 2
    portal_w = dict()
    for r, c in set(portal_ch.keys()):
        if (r, c) in portal_ch and (r + 1, c) in portal_ch:
            key = portal_ch.pop((r, c)) + portal_ch.pop((r + 1, c))
            doors = portal_w.setdefault(key, [])
            if maze.get((r + 2, c), False):
                doors.append((r + 2, c))
            elif maze.get((r - 1, c), False):
                doors.append((r - 1, c))
            else:
                assert False
        elif (r, c) in portal_ch and (r, c + 1) in portal_ch:
            key = portal_ch.pop((r, c)) + portal_ch.pop((r, c + 1))
            doors = portal_w.setdefault(key, [])
            if maze.get((r, c + 2), False):
                doors.append((r, c + 2))
            elif maze.get((r, c - 1), False):
                doors.append((r, c - 1))
            else:
                assert False
    assert not portal_ch
    assert len(portal_w["AA"]) == 1 and len(portal_w["ZZ"]) == 1
    start = portal_w.pop("AA")[0]
    end = portal_w.pop("ZZ")[0]
    assert all(len(d) == 2 for d in portal_w.values())
    board = np.zeros(shape=(row_max + 2, col_max + 2), dtype=bool)
    for (r, c), _ in filter(lambda kv: kv[1], maze.items()):
        board[r, c] = True
    portals = dict()
    for d in portal_w.values():
        portals[d[0]] = (d[1], is_edge(d[0]))
        portals[d[1]] = (d[0], is_edge(d[1]))
    return start, end, board, portals


START, END, BOARD, PORTALS = parse(
    map(lambda x: x.rstrip(), open("20.txt", "r").readlines())
)


def neighbours_pt(pt):
    yield pt[0] - 1, pt[1]
    yield pt[0] + 1, pt[1]
    yield pt[0], pt[1] - 1
    yield pt[0], pt[1] + 1


def bfs(start, end, neighbour_fn):
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        curr, dist = queue.popleft()
        if curr == end:
            return dist
        for n in neighbour_fn(curr):
            if n in visited:
                continue
            visited.add(n)
            queue.append((n, dist + 1))
    return None


def neighbours(pt, board, portals):
    if pt in portals:
        yield portals[pt][0]
    for n in neighbours_pt(pt):
        if board[n]:
            yield n


# part 1
print(bfs(START, END, partial(neighbours, board=BOARD, portals=PORTALS)))


def neighbours_rec(pt_lvl, board, portals):
    pt, lvl = pt_lvl
    if pt in portals:
        tar, out = portals[pt]
        if not out:
            yield tar, lvl + 1
        elif lvl > 0:
            yield tar, lvl - 1
    for n in neighbours_pt(pt):
        if board[n]:
            yield n, lvl


# part 2
print(bfs((START, 0), (END, 0), partial(neighbours_rec, board=BOARD, portals=PORTALS)))
