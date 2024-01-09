import intcode

CODE = list(map(int, open("19.txt", "r").read().strip().split(",")))

comp = intcode.Computer(CODE)


def beam(col, row):
    return comp.reset().run_to_output(col, row)


# part 1
print(
    sum(comp.reset().run_to_output(col, row) for row in range(50) for col in range(50))
)


def find_last_before_beam(_x, _y):
    assert beam(_x, _y) == 0
    while beam(_x, _y) == 0:
        _y += 1
    return _y - 1


def find_last_in_beam(_x, _y):
    assert beam(_x, _y) == 1
    while beam(_x, _y) == 1:
        _y += 1
    return _y - 1


# approximate lines with rational numbers
# beam edge equations: y = c1*x and y = c2*x
x = 10
c2 = find_last_before_beam(x, 0) / x
c1 = find_last_in_beam(x, int(x * c2) + 1) / x

for i in range(2, 10):
    x = 10**i
    c2 = find_last_before_beam(x, int(x * c2)) / x
    c1 = find_last_in_beam(x, int(x * c1)) / x


# solve equation to find approximate points
# opposite corners of square: (x1, y1) and (x2, y2)
# corners are on different edges: y1=c1*x1, y2=c2*x2
# corners are on -1 slope diagonal: (x2-x1) = -(y2-y1)
# side lengths are 100: x2-x1 = 100, y1-y2 = 100
#
# x2-x1 = y1-y2 = c1*x1 - c2*x2 => x2 = x1*(c1+1)/(c2+1)
# x2-x1 = 100 => x1*( (1+c1)/(1+c2) - 1) = 100
k = (c1 + 1) / (c2 + 1)
x1 = 100 / (k - 1)
x2 = x1 * k
y1 = c1 * x1
y2 = c2 * x2

assert int(x2) == int(x1) + 100 and int(y1) == int(y2) + 100

x, y = int(x1), int(y2)


def width_at_least(_x, _y, w):
    return beam(_x + w - 1, _y) == 1


def height_at_least(_x, _y, h):
    return beam(_x, _y + h - 1) == 1


# go further until beam width/height is enough
while not (width_at_least(x, y, 100) and height_at_least(x, y, 100)):
    y += 1
    x += 1

# go back until beam width/height cannot shrink anymore
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
