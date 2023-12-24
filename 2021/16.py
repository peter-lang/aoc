from typing import Iterator
from itertools import islice
from functools import reduce
import operator

txt = open("16.txt", "r").read().strip()

hex2bin = {hex(i)[2:].upper(): bin(i)[2:].zfill(4) for i in range(16)}


def asbin(it: Iterator[str]):
    for i in it:
        for ch in hex2bin[i]:
            yield ch


def parse_txt(it: Iterator[str], length: int) -> str:
    txt = "".join(islice(it, length))
    if len(txt) < length:
        raise StopIteration
    return txt


def parse_num(it: Iterator[str], length: int) -> int:
    return int(parse_txt(it, length), 2)


def parse(it: Iterator[str]) -> tuple:
    try:
        while True:
            version = parse_num(it, 3)
            type_id = parse_num(it, 3)
            if type_id == 4:
                num_bits = []
                while parse_txt(it, 1) == "1":
                    num_bits += parse_txt(it, 4)
                num_bits += parse_txt(it, 4)
                value = int("".join(num_bits), 2)
                yield version, type_id, value
            else:
                length_type_id = parse_txt(it, 1)
                if length_type_id == "0":
                    length = parse_num(it, 15)
                    yield version, type_id, list(parse(islice(it, length)))
                else:
                    length = parse_num(it, 11)
                    yield version, type_id, list(islice(parse(it), length))
    except StopIteration:
        return


def sum_version_ids(packet):
    version, type_id, value = packet
    if isinstance(value, list):
        return version + sum(sum_version_ids(p) for p in value)
    else:
        return version


def evaluate(packet):
    version, type_id, value = packet
    if type_id == 4:
        return value
    elif type_id == 0:
        return sum(evaluate(p) for p in value)
    elif type_id == 1:
        return reduce(operator.mul, (evaluate(p) for p in value))
    elif type_id == 2:
        return min(evaluate(p) for p in value)
    elif type_id == 3:
        return max(evaluate(p) for p in value)
    elif type_id == 5:
        return 1 if evaluate(value[0]) > evaluate(value[1]) else 0
    elif type_id == 6:
        return 1 if evaluate(value[0]) < evaluate(value[1]) else 0
    elif type_id == 7:
        return 1 if evaluate(value[0]) == evaluate(value[1]) else 0


# part 1
print(sum(sum_version_ids(p) for p in parse(asbin(iter(txt)))))

# part 2
print(*(evaluate(p) for p in parse(asbin(iter(txt)))))
