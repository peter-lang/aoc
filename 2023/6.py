import math
from functools import reduce

num_lines = list(
    map(
        lambda x: x.split(":")[1].strip(),
        filter(None, map(lambda x: x.strip(), open("6.txt", "r").readlines())),
    )
)


def hold_time_dur(t_best, dist):
    # x := pressing time, x > 0
    # t_best > t_total = x + dist / x
    # 0 > x**2 - t_best * x + dist
    discriminant = math.sqrt(t_best**2 - 4 * dist)
    # x_min smallest int: x_min > (t_best - discriminant) / 2
    x_min = math.floor((t_best - discriminant) * 0.5) + 1
    # x_max biggest int : x_max < (t_best + discriminant) / 2
    x_max = math.ceil((t_best + discriminant) * 0.5) - 1
    interval_length = x_max - x_min + 1
    return interval_length


# part 1
time_dists = zip(*(map(lambda x: int(x.strip()), line.split()) for line in num_lines))
print(
    reduce(
        lambda a, b: a * b, (hold_time_dur(*time_dist) for time_dist in time_dists), 1
    )
)

# part 2
single_time_dist = (int(line.replace(" ", "")) for line in num_lines)
print(hold_time_dur(*single_time_dist))
