import intcode

CODE = list(map(int, open("13.txt", "r").read().strip().split(",")))


def sign(v):
    if v < 0:
        return -1
    if v > 0:
        return 1
    return 0


class BlockBreaker:
    def __init__(self, code):
        self.comp = intcode.Computer([2] + code[1:]).reset()
        self.walls = set()
        self.blocks = set()
        self.ball = None
        self.ball_dir = None
        self.paddle = (-1, -1)
        self.score = 0

    def play_until_input(self):
        while True:
            try:
                while (outs := self.comp.run_to_outputs(3)) is not None:
                    c, r, t = outs
                    if c == -1 and r == 0:
                        self.score = t
                    elif t == 0:
                        self.blocks.discard((r, c))
                    elif t == 1:
                        self.walls.add((r, c))
                    elif t == 2:
                        self.blocks.add((r, c))
                    elif t == 3:
                        self.paddle = (r, c)
                    elif t == 4:
                        if self.ball is not None:
                            self.ball_dir = (r - self.ball[0], c - self.ball[1])
                        self.ball = (r, c)
                return self.score
            except intcode.WaitForInput:
                return None

    def play(self):
        while (res := self.play_until_input()) is None:
            if self.ball_dir is None:
                self.comp.inputs.append(0)
            else:
                if self.ball[0] < self.paddle[0] - 1:
                    ball_next = (
                        self.ball[0] + self.ball_dir[0],
                        self.ball[1] + self.ball_dir[1],
                    )
                    self.comp.inputs.append(sign(ball_next[1] - self.paddle[1]))
                else:
                    self.comp.inputs.append(sign(self.ball[1] - self.paddle[1]))

        return res


# part 1
COMP = intcode.Computer(CODE).reset()
blocks = 0
while (outs := COMP.run_to_outputs(3)) is not None:
    c, r, t = outs
    if t == 2:
        blocks += 1
print(blocks)


# part 2
game = BlockBreaker(CODE)
print(game.play())
