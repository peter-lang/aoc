board = [
    [int(ch) for ch in row]
    for row in map(lambda x: x.strip(), open("8.txt", "r").readlines())
]

MAX_ROW = len(board)
MAX_COL = len(board[0])


# part 1
def visibility_map():
    result = [[False] * MAX_COL for _ in range(MAX_ROW)]
    for r in range(MAX_ROW):
        result[r][0] = True
        v = board[r][0]
        for i in range(1, MAX_COL):
            if board[r][i] > v:
                result[r][i] = True
                v = board[r][i]
        result[r][-1] = True
        v = board[r][-1]
        for i in range(MAX_COL - 2, -1, -1):
            if board[r][i] > v:
                result[r][i] = True
                v = board[r][i]
    for c in range(MAX_COL):
        result[0][c] = True
        v = board[0][c]
        for i in range(1, MAX_ROW):
            if board[i][c] > v:
                result[i][c] = True
                v = board[i][c]
        result[-1][c] = True
        v = board[-1][c]
        for i in range(MAX_ROW - 2, -1, -1):
            if board[i][c] > v:
                result[i][c] = True
                v = board[i][c]
    return result


print(sum(cell for row in visibility_map() for cell in row))


# part 2
def line_of_sight(r, c):
    up = next((r - i for i in range(r - 1, -1, -1) if board[i][c] >= board[r][c]), r)
    left = next((c - i for i in range(c - 1, -1, -1) if board[r][i] >= board[r][c]), c)
    down = next(
        (i - r for i in range(r + 1, MAX_ROW) if board[i][c] >= board[r][c]),
        MAX_ROW - r - 1,
    )
    right = next(
        (i - c for i in range(c + 1, MAX_COL) if board[r][i] >= board[r][c]),
        MAX_COL - c - 1,
    )
    return up, left, down, right


def score(r, c):
    up, left, down, right = line_of_sight(r, c)
    return up * left * down * right


print(max(score(r, c) for r in range(MAX_ROW) for c in range(MAX_COL)))
