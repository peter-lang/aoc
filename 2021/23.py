import heapdict
from typing import Iterator
from functools import reduce
from collections import deque
import math

COORD = tuple[int, int]
AMPHIPOD = frozenset[COORD, ...]
AMPHIPODS = tuple[AMPHIPOD, ...]

LINES = list(filter(None, map(lambda x: x.rstrip(), open("23.txt", "r").readlines())))

# positions:
# empty line: row = 0, col = 0..10 (4 stack, 3 in-between, 2*2 wing)
# stack-positions: row = 1..n, col = {2, 4, 6, 8}


def parse_start(lines) -> AMPHIPODS:
    result = [[] for _ in range(4)]
    for row in range(2, len(lines) - 1):
        for col in (3, 5, 7, 9):
            result[ord(lines[row][col]) - ord("A")].append((row - 1, col - 1))
    return tuple(frozenset(r) for r in result)


def pt_neighbour(pt: COORD, stack_size: int) -> Iterator[COORD]:
    if pt[0] == 0:
        if pt[1] == 0:  # left-end
            yield pt[0], pt[1] + 1
        elif pt[1] == 10:  # right-end
            yield pt[0], pt[1] - 1
        else:  # in-between
            yield pt[0], pt[1] + 1
            yield pt[0], pt[1] - 1
            if pt[1] in (2, 4, 6, 8):  # above stacks
                yield pt[0] + 1, pt[1]
    elif pt[0] == stack_size:
        yield pt[0] - 1, pt[1]
    else:
        yield pt[0] - 1, pt[1]
        yield pt[0] + 1, pt[1]


def stack_pos(pt: COORD) -> tuple[int, int] | None:
    if pt[0] >= 1:
        return pt[1] // 2 - 1, pt[0] - 1
    return None


above_stacks = {(0, (i + 1) * 2) for i in range(4)}


def bfs_neighbours(
    pt: COORD, occupied: frozenset[COORD], stack_size: int
) -> dict[COORD, int]:
    visited = dict()
    open_set = deque([(pt, 0)])
    while open_set:
        curr, dist = open_set.popleft()
        if curr in visited:
            continue
        visited[curr] = dist
        for n in pt_neighbour(curr, stack_size):
            if n in occupied:
                continue
            open_set.append((n, dist + 1))
    del visited[pt]
    return visited


def to_occupied(state: AMPHIPODS) -> frozenset[COORD]:
    return reduce(lambda a, b: a | b, state)


def heuristic(current: AMPHIPODS, target: AMPHIPODS) -> int:
    total = 0
    for idx, (curr, tar) in enumerate(zip(current, target)):
        unfilled_tar = list(tar - curr)
        unmatched_curr = list(curr - tar)
        for c, t in zip(unmatched_curr, unfilled_tar):
            # we need to move at least up to the empty line then to the right col and the right row
            least_moves = abs(c[0] - 0) + abs(c[1] - t[1]) + abs(t[0] - 0)
            total += least_moves * 10**idx
    return total


def moves(current: AMPHIPODS, stack_size: int) -> Iterator[tuple[AMPHIPODS, int]]:
    occupied = to_occupied(current)
    stacks = [[None] * stack_size for _ in range(4)]
    for type_idx, amphs in enumerate(current):
        for src in amphs:
            if (p := stack_pos(src)) is not None:
                c, r = p
                stacks[c][r] = type_idx

    for type_idx, amphs in enumerate(current):
        for src in amphs:
            src_sp = stack_pos(src)
            if (
                src_sp is not None
                and src_sp[0] == type_idx
                and all(el == type_idx for el in stacks[src_sp[0]][src_sp[1] :])
            ):
                # if part of properly filled stack => don't move
                continue

            remaining = amphs - {src}
            move_targets = bfs_neighbours(src, occupied, stack_size)
            for dst, distance in move_targets.items():
                dst_sp = stack_pos(dst)
                if dst_sp is None:
                    if src_sp is None:
                        # do not allow out-of-stack to out-of-stack move
                        continue
                    elif dst in above_stacks:
                        # stack to above-stack is not allowed
                        continue
                else:
                    c, r = dst_sp
                    if c != type_idx:
                        # do not move to other stack
                        continue
                    if any(stacks[c][sr] != c for sr in range(r + 1, stack_size)):
                        # do not move to top of stack, if it contains wrong element below
                        continue

                moved_state = (
                    current[:type_idx]
                    + (remaining | {dst},)
                    + current[(type_idx + 1) :]
                )
                cost = distance * 10**type_idx
                yield moved_state, cost


def a_star(start: AMPHIPODS, end: AMPHIPODS, stack_size: int):
    open_set = heapdict.heapdict()
    open_set[start] = heuristic(start, end)

    g_score = dict()
    g_score[start] = 0

    while open_set:
        current, _ = open_set.popitem()
        if current == end:
            return g_score[current]

        for child, cost in moves(current, stack_size):
            tentative_g_score = g_score[current] + cost
            prev = g_score.get(child, math.inf)
            if tentative_g_score < prev:
                g_score[child] = tentative_g_score
                open_set[child] = tentative_g_score + heuristic(child, end)
    return None


# part 1
p1_start = parse_start(LINES)
p1_target = tuple(frozenset((r, c) for r in range(1, 3)) for c in (2, 4, 6, 8))
print(a_star(p1_start, p1_target, 2))


# part 2
EXTRA_LINES = ["  #D#C#B#A#", "  #D#B#A#C#"]
p2_start = parse_start(LINES[:3] + EXTRA_LINES + LINES[3:])
p2_target = tuple(frozenset((r, c) for r in range(1, 5)) for c in (2, 4, 6, 8))
print(a_star(p2_start, p2_target, 4))
