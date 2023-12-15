seq = open("15.txt", "r").read().split(",")


def comp_hash(s: str) -> int:
    val = 0
    for ch in s:
        val += ord(ch)
        val *= 17
        val %= 256
    return val


# part 1
print(sum(comp_hash(el) for el in seq))


# part 2
def parts(s: str) -> tuple[str, int | None]:
    if s.endswith("-"):
        return s[:-1], None
    else:
        label, value = s.split("=")
        return label, int(value)


def execute_order(boxes, order):
    label, value = parts(order)
    idx = comp_hash(label)
    box = boxes[idx]
    if value is None:
        if label in box:
            del box[label]
    else:
        box[label] = value


BOXES: list[dict[str, int]] = [dict() for _ in range(256)]

for el in seq:
    execute_order(BOXES, el)

print(
    sum(
        (idx + 1) * (v_idx + 1) * v
        for idx, b in enumerate(BOXES)
        for v_idx, v in enumerate(b.values())
    )
)
