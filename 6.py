import math
from functools import reduce

num_lines = list(
    map(
        lambda x: x[len("Distance:"):].strip(),
        filter(None, map(lambda x: x.strip(), open("6.txt", "r").readlines()))
    )
)

eps = 1e-12


def hold_time_dur(min_time, dist):
    discriminant = math.sqrt(min_time ** 2 - 4 * dist)
    min_hold_time = math.ceil((min_time - discriminant) * 0.5 + eps)
    max_hold_time = math.floor((min_time + discriminant) * 0.5 - eps)
    return max_hold_time - min_hold_time + 1


# part 1
time_dists = zip(*(map(lambda x: int(x.strip()), line.split()) for line in num_lines))
print(reduce(lambda a, b: a * b, (hold_time_dur(*time_dist) for time_dist in time_dists), 1))

# part 2
single_time_dist = (int(line.replace(" ", "")) for line in num_lines)
print(hold_time_dur(*single_time_dist))
