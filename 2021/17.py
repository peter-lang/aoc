import re
import math

pattern = re.compile(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)")

match = pattern.match(open("17.txt", "r").read().strip())
x_min, x_max = int(match.group(1)), int(match.group(2))
y_min, y_max = int(match.group(3)), int(match.group(4))

# part 1
max_y_v = -y_min - 1
print((max_y_v + 1) * max_y_v // 2)

# part 2
min_x_v = math.ceil(0.5 * (math.sqrt(1 + 4 * 2 * x_min)) - 1)
# every positive y_v has a negative pair:
# 0 -> -1, 1 -> -2, max_y_v -> -max_y_v-1

v_pairs = set()
for y_v in range(-max_y_v - 1, max_y_v + 1):
    if y_v >= 0:
        y_t_offset = y_v + 1
        y_start = -y_v - 1
    else:
        y_t_offset = y_v + 1
        y_start = y_v
    y_offset = (y_start + 1) * y_start
    y_t_min = math.ceil(0.5 * (math.sqrt(1 + 4 * (2 * (-y_max) + y_offset)) - 1))
    y_t_max = math.floor(0.5 * (math.sqrt(1 + 4 * (2 * (-y_min) + y_offset)) - 1))
    if y_v == 7:
        pass

    for t in range(y_t_offset + y_t_min, y_t_offset + y_t_max + 1):
        assert y_min <= sum((y_v - i) for i in range(t)) <= y_max
        x_v = 0
        # TODO: there is probably a better formula for f=this
        while sum(x_v - i for i in range(min(t, x_v))) < x_min:
            x_v += 1
        while sum(x_v - i for i in range(min(t, x_v))) <= x_max:
            v_pairs.add((x_v, y_v))
            x_v += 1

print(len(v_pairs))
