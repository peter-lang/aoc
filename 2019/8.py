import numpy as np

digits = list(map(int, open("8.txt", "r").read().strip()))

IMAGES = np.array(digits).reshape((-1, 6, 25))


def combine(images):
    res = np.full_like(images[0], 2)
    for idx in range(images.shape[0]):
        res_tpt = res == 2
        if np.count_nonzero(res_tpt) == 0:
            return res
        res[res_tpt & (images[idx] == 0)] = 0
        res[res_tpt & (images[idx] == 1)] = 1
    return res


# part 1
_, p1_img_idx = min(
    (np.count_nonzero(IMAGES[idx] == 0), idx) for idx in range(IMAGES.shape[0])
)
print(
    np.count_nonzero(IMAGES[p1_img_idx] == 1)
    * np.count_nonzero(IMAGES[p1_img_idx] == 2)
)


# part 2
dec = {0: " ", 1: "#"}
for row in combine(IMAGES):
    print("".join(dec[ch] for ch in row))
