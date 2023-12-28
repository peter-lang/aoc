import numpy as np

lines = list(filter(None, map(lambda x: x.strip(), open("20.txt", "r").readlines())))

codec_table = np.array([v == "#" for v in lines[0]], dtype=np.uint16)

board = np.array([[v == "#" for v in line] for line in lines[1:]], dtype=np.uint16)


def codec(v):
    return codec_table[v]


codec_vec = np.vectorize(codec)


def enhance_2(b: np.array, one_filled: bool):
    b = np.pad(b, ((2, 2), (2, 2)), constant_values=1 if one_filled else 0)
    res = np.array(
        [
            [
                codec_table[
                    int(
                        "".join(
                            str(ch)
                            for ch in b[(r - 1) : (r + 2), (c - 1) : (c + 2)].ravel()
                        ),
                        2,
                    )
                ]
                for c in range(1, b.shape[0] - 1)
            ]
            for r in range(1, b.shape[0] - 1)
        ]
    )
    return res, bool(codec_table[-1]) if one_filled else bool(codec_table[0])


def enhance(b: np.array, one_filled: bool):
    acc = np.zeros((b.shape[0] + 2, b.shape[1] + 2), dtype=np.uint16)
    if one_filled:
        assert acc.shape[0] >= 4 and acc.shape[1] >= 4
        # top
        acc[0, 0] = 511 - 1
        acc[0, 1] = 511 - (2 + 1)
        acc[0, 2:-2] = 511 - (4 + 2 + 1)
        acc[0, -2] = 511 - (4 + 2)
        acc[0, -1] = 511 - 4
        #
        acc[1, 0] = 511 - (8 + 1)
        acc[1, 1] = 511 - (16 + 8 + 2 + 1)
        acc[1, 2:-2] = 511 - (32 + 16 + 8 + 4 + 2 + 1)
        acc[1, -2] = 511 - (32 + 16 + 4 + 2)
        acc[1, -1] = 511 - (32 + 4)

        # bottom
        acc[-1, 0] = 511 - 64
        acc[-1, 1] = 511 - (128 + 64)
        acc[-1, 2:-2] = 511 - (256 + 128 + 64)
        acc[-1, -2] = 511 - (256 + 128)
        acc[-1, -1] = 511 - 256
        acc[-2, 0] = 511 - (64 + 8)
        acc[-2, 1] = 511 - (128 + 64 + 16 + 8)
        acc[-2, 2:-2] = 511 - (256 + 128 + 64 + 32 + 16 + 8)
        acc[-2, -2] = 511 - (256 + 128 + 32 + 16)
        acc[-2, -1] = 511 - (256 + 32)

        # left
        acc[2:-2, 0] = 511 - (64 + 8 + 1)
        acc[2:-2, 1] = 511 - (128 + 64 + 16 + 8 + 2 + 1)

        # right
        acc[2:-2, -1] = 511 - (256 + 32 + 4)
        acc[2:-2, -2] = 511 - (256 + 128 + 32 + 16 + 4 + 2)

    # 256 128 64
    #  32  16  8
    #   4   2  1
    acc[2:, 2:] += 256 * b
    acc[2:, 1:-1] += 128 * b
    acc[2:, :-2] += 64 * b
    acc[1:-1, 2:] += 32 * b
    acc[1:-1, 1:-1] += 16 * b
    acc[1:-1, :-2] += 8 * b
    acc[:-2, 2:] += 4 * b
    acc[:-2, 1:-1] += 2 * b
    acc[:-2, :-2] += 1 * b
    res = codec_vec(acc)
    return res, bool(codec_table[-1]) if one_filled else bool(codec_table[0])


def multi_enhance(b: np.array, one_filled: bool, n: int) -> np.array:
    for _ in range(n):
        b, one_filled = enhance(b, one_filled)
    return b


# part 1
print(multi_enhance(board, False, 2).sum())

# part 2
print(multi_enhance(board, False, 50).sum())
