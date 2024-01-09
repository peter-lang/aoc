import numpy as np

lines = filter(None, map(lambda x: x.strip(), open("24.txt", "r").readlines()))
BOARD = np.array([[ch == "#" for ch in line] for line in lines], dtype=np.uint8)


def update_until_visited(board):
    board = np.pad(board, ((1, 1), (1, 1)))

    def update(B: np.array):
        N = np.zeros_like(B)
        N[1:-1, 1:-1] = B[:-2, 1:-1] + B[2:, 1:-1] + B[1:-1, :-2] + B[1:-1, 2:]

        birth = ((N == 1) | (N == 2)) & (B == 0)
        survive = (N == 1) & (B == 1)
        B[...] = 0
        B[birth | survive] = 1
        return B

    def to_int(B: np.array):
        vals = B[1:-1, 1:-1].ravel()
        return sum(v * 2**idx for idx, v in enumerate(vals))

    visited = {to_int(board)}

    while True:
        board = update(board)
        chksum = to_int(board)
        if chksum in visited:
            return chksum
        else:
            visited.add(chksum)


# part 1
print(update_until_visited(BOARD))

MID = 3


class RecursiveBoard:
    def __init__(self, board, parent=None, child=None):
        self.B = board
        self.N = None
        self.parent = parent
        self.child = child

    def update_neighbours(self, rec_dir):
        self.N = np.zeros_like(self.B)
        self.N[1:-1, 1:-1] = (
            self.B[:-2, 1:-1] + self.B[2:, 1:-1] + self.B[1:-1, :-2] + self.B[1:-1, 2:]
        )

        # add parent values
        if self.parent is not None:
            # top edge
            self.N[1, 1:-1] += self.parent.B[MID - 1, MID]
            # left edge
            self.N[1:-1, 1] += self.parent.B[MID, MID - 1]
            # right edge
            self.N[1:-1, -2] += self.parent.B[MID, MID + 1]
            # bottom edge
            self.N[-2, 1:-1] += self.parent.B[MID + 1, MID]
            if rec_dir >= 0:
                self.parent.update_neighbours(1)
        elif (
            np.any(self.B[1, 1:-1] > 0)
            or np.any(self.B[-2, 1:-1] > 0)
            or np.any(self.B[1:-1, 1] > 0)
            or np.any(self.B[1:-1, -2] > 0)
        ):
            self.parent = RecursiveBoard(np.zeros_like(self.B), child=self)
            if rec_dir >= 0:
                self.parent.update_neighbours(1)

        if self.child is not None:
            # top
            self.N[MID - 1, MID] += self.child.B[1, 1:-1].sum()
            # left
            self.N[MID, MID - 1] += self.child.B[1:-1, 1].sum()
            # right
            self.N[MID, MID + 1] += self.child.B[1:-1, -2].sum()
            # bottom
            self.N[MID + 1, MID] += self.child.B[-2, 1:-1].sum()
            if rec_dir <= 0:
                self.child.update_neighbours(-1)
        elif (
            self.B[MID - 1, MID] > 0
            or self.B[MID, MID - 1] > 0
            or self.B[MID, MID + 1] > 0
            or self.B[MID + 1, MID]
        ):
            self.child = RecursiveBoard(np.zeros_like(self.B), parent=self)
            if rec_dir <= 0:
                self.child.update_neighbours(-1)

    def update_board(self, rec_dir):
        birth = ((self.N == 1) | (self.N == 2)) & (self.B == 0)
        survive = (self.N == 1) & (self.B == 1)
        self.B[...] = 0
        self.B[birth | survive] = 1
        self.B[MID, MID] = 0
        if rec_dir >= 0 and self.parent is not None:
            self.parent.update_board(1)
        if rec_dir <= 0 and self.child is not None:
            self.child.update_board(-1)

    def update(self, rec_dir=0):
        self.update_neighbours(rec_dir)
        self.update_board(rec_dir)

    def sum(self, rec_dir=0):
        total = self.B.sum()
        if rec_dir >= 0 and self.parent is not None:
            total += self.parent.sum(1)
        if rec_dir <= 0 and self.child is not None:
            total += self.child.sum(-1)
        return total


# part 2
rec_board = RecursiveBoard(board=np.pad(BOARD, ((1, 1), (1, 1))))
for _ in range(200):
    rec_board.update()
print(rec_board.sum())
