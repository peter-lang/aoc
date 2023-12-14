import numpy as np
from fractions import Fraction

sequences = [
    np.array(list(map(lambda x: int(x.strip()), line.split())))
    for line in filter(None, map(lambda x: x.strip(), open("9.txt", "r").readlines()))
]


# part 1
def predict_forward(seq):
    if len(seq) == 0 or not np.any(seq):
        return 0
    return seq[-1] + predict_forward(seq[1:] - seq[:-1])


print(sum(predict_forward(s) for s in sequences))


# part 2
def predict_backward(seq):
    if len(seq) == 0 or not np.any(seq):
        return 0
    return seq[0] - predict_backward(seq[1:] - seq[:-1])


print(sum(predict_backward(s) for s in sequences))


# extra (see: https://www.youtube.com/watch?v=4AuV93LOPcE&t=2412s )
def polynomial_formula(seq):
    coefficient = []
    while len(seq) > 0 and np.any(seq):
        coefficient.append(seq[0])
        seq = seq[1:] - seq[:-1]

    binomial_polynom = np.zeros(len(coefficient), dtype=int) + Fraction()
    binomial_polynom[-1] = 1
    result = coefficient[0] * binomial_polynom

    for deg in range(1, len(coefficient)):
        binomial_polynom = np.roll(binomial_polynom, -1) - (deg - 1) * binomial_polynom
        binomial_polynom = binomial_polynom / deg
        result += coefficient[deg] * binomial_polynom
    return result


# poly = polynomial_formula(np.array([1, 2, 4, 8, 16]))
# print(np.polyval(poly, 5), np.polyval(poly, 6))  # 31, 57, ...
