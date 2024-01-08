import intcode

CODE = list(map(int, open("19.txt", "r").read().strip().split(",")))

comp = intcode.Computer(CODE)


def beam(col, row):
    return comp.reset().run_to_output(col, row)


# part 1
print(
    sum(comp.reset().run_to_output(col, row) for row in range(50) for col in range(50))
)


def find_min(x, y):
    assert beam(x, y) == 0
    while beam(x, y) == 0:
        y += 1
    return y - 1


def find_max(x, y):
    assert beam(x, y) == 1
    while beam(x, y) == 1:
        y += 1
    return y - 1


# approximate lines with rational numbers
x = 10
c2 = find_min(x, 0) / x
c1 = find_max(x, int(x * c2) + 1) / x

for i in range(2, 10):
    x = 10**i
    c2 = find_min(x, int(x * c2)) / x
    c1 = find_max(x, int(x * c1)) / x

# solve equation to find approximate points
k = (c1 + 1) / (c2 + 1)
x1 = 100 / (k - 1)
x2 = x1 * k
y1 = c1 * x1
y2 = c2 * x2


x, y = min(int(x1), int(x2)), min(int(y2), int(y1))


def width_at_least(x, y, w):
    return beam(x + w - 1, y) == 1


def height_at_least(x, y, h):
    return beam(x, y + h - 1) == 1


assert width_at_least(x, y, 100) and height_at_least(x, y, 100)

# gradually fine-tune minimal location
while True:
    if width_at_least(x - 1, y - 1, 100) and height_at_least(x - 1, y - 1, 100):
        y -= 1
        x -= 1
        continue
    if width_at_least(x - 1, y, 100) and height_at_least(x - 1, y, 100):
        x -= 1
        continue
    if width_at_least(x, y - 1, 100) and height_at_least(x, y - 1, 100):
        y -= 1
        continue
    break

# part 2
print(x * 10000 + y)
