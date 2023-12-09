import numpy as np

sequences = [
    np.array(list(map(lambda x: int(x.strip()), line.split())))
    for line in filter(None, map(lambda x: x.strip(), open("9.txt", "r").readlines()))
]


# part 1
def predict_forward(seq):
    if len(seq) == 0 or np.all(seq == 0):
        return 0
    return seq[-1] + predict_forward(seq[1:] - seq[:-1])


print(sum(predict_forward(s) for s in sequences))


# part 2
def predict_backward(seq):
    if len(seq) == 0 or np.all(seq == 0):
        return 0
    return seq[0] - predict_backward(seq[1:] - seq[:-1])


print(sum(predict_backward(s) for s in sequences))
