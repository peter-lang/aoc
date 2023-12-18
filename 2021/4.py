from itertools import islice
from collections import defaultdict

lines = list(filter(None, map(lambda x: x.strip(), open("4.txt", "r").readlines())))

BOARD_LEN = 5


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


DRAWN = list(map(int, lines[0].split(",")))
BOARDS = [[list(map(int, r.split())) for r in b] for b in batched(lines[1:], BOARD_LEN)]


def board_scores(boards, drawn):
    rows = [[0] * BOARD_LEN for _ in boards]
    cols = [[0] * BOARD_LEN for _ in boards]
    nums = defaultdict(list)
    for board_idx, board in enumerate(boards):
        for row in range(BOARD_LEN):
            for col in range(BOARD_LEN):
                nums[board[row][col]].append((board_idx, row, col))
    total = set()

    playing = set(range(len(boards)))
    result = []

    for d in drawn:
        total.add(d)
        for b_idx, r, c in nums[d]:
            rows[b_idx][r] += 1
            cols[b_idx][c] += 1
            if b_idx in playing and (rows[b_idx][r] == 5 or cols[b_idx][c] == 5):
                result.append(
                    d * sum(v for r in boards[b_idx] for v in r if v not in total)
                )
                playing.remove(b_idx)
                if not playing:
                    return result


scores = board_scores(BOARDS, DRAWN)

# part 1
print(scores[0])

# part 2
print(scores[-1])
