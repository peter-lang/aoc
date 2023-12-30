import re
from functools import cache

containee_pattern = re.compile("(\d+) (.*) bags?")


def parse_containees(txt):
    if txt == "no other bags":
        return []
    result = []
    for containee in txt.split(", "):
        m = containee_pattern.match(containee)
        result.append((int(m.group(1)), m.group(2)))
    return result


contains = {}
for line in filter(None, map(lambda x: x.strip(), open("7.txt", "r").readlines())):
    line = line[:-1]  # remove dot
    container, containees = line.split(" contain ")
    assert container.endswith(" bags")
    container = container[:-5]
    contains[container] = parse_containees(containees)


@cache
def might_contain(src, dst):
    children = set(col for cnt, col in contains[src])
    if dst in children:
        return True
    else:
        return any(might_contain(child, dst) for child in children)


@cache
def must_contain(src):
    return sum(cnt * must_contain(col) for cnt, col in contains[src]) + 1


# part 1
print(sum(might_contain(col, "shiny gold") for col in contains))

# part 2
print(must_contain("shiny gold") - 1)
