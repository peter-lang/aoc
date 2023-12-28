from functools import cache

p1_start = 4
p2_start = 1


def play_game(pos):
    score = [0 for _ in pos]
    p = 1
    dice = 1
    rolls = 0
    while True:
        forward = 0
        for _ in range(3):
            forward += dice
            dice = dice % 100 + 1
            rolls += 1

        n = (p + 1) % 2
        pos[n] = (pos[n] + forward - 1) % 10 + 1
        score[n] += pos[n]
        if score[n] >= 1000:
            return score[p] * rolls
        p = n


forwards_3d3 = [1, 3, 6, 7, 6, 3, 1]


@cache
def play_dirac_game(p1_pos, p2_pos, p1_sc, p2_sc):
    p1_w, p2_w = 0, 0
    for fwd_offset, worlds in enumerate(forwards_3d3):
        fwd = fwd_offset + 3
        p1_next_pos = (p1_pos + fwd - 1) % 10 + 1
        p1_next_sc = p1_sc + p1_next_pos
        if p1_next_sc >= 21:
            p1_w += worlds
        else:
            p2_rec_w, p1_rec_w = play_dirac_game(p2_pos, p1_next_pos, p2_sc, p1_next_sc)
            p1_w += worlds * p1_rec_w
            p2_w += worlds * p2_rec_w
    return p1_w, p2_w


# part 1
print(play_game([p1_start, p2_start]))


# part 2
print(max(play_dirac_game(p1_start, p2_start, 0, 0)))
