from itertools import chain

lines = filter(None, map(lambda x: x.strip(), open("14.txt", "r").readlines()))


def parse_line(line) -> tuple[list[tuple[int, str]], tuple[int, str]]:
    def cnt_prd(txt):
        cnt, prd = txt.split(" ")
        return int(cnt), prd

    src, dst = line.split(" => ")
    return [cnt_prd(el) for el in src.split(", ")], cnt_prd(dst)


productions = list(map(parse_line, lines))


all_nodes = {
    prod_node[1]
    for prod_nodes in (chain([target], sources) for sources, target in productions)
    for prod_node in prod_nodes
}

consume_edges = {
    target[1]: [source[1] for source in sources] for sources, target in productions
}

consumes_counts = {target[1]: (target[0], sources) for sources, target in productions}


def reverse_edges(edges):
    res = dict()
    for n, child in edges.items():
        for ch in child:
            res.setdefault(ch, []).append(n)
    return res


produce_edges = reverse_edges(consume_edges)


def topological_sort(nodes: set, edges: dict) -> list:
    sorted_nodes = []
    permanent_mark = set()
    tmp_mark = set()

    def visit(n):
        if n in permanent_mark:
            return
        assert n not in tmp_mark
        tmp_mark.add(n)
        for child in edges.get(n, []):
            visit(child)
        tmp_mark.remove(n)
        permanent_mark.add(n)
        sorted_nodes.append(n)

    while nodes:
        visit(nodes.pop())
    return sorted_nodes


top_sorted = topological_sort(set(all_nodes), produce_edges)
assert top_sorted[0] == "FUEL"
assert top_sorted[-1] == "ORE"


def reduce_to_ore(reqs):
    for mat in top_sorted[:-1]:
        cnt = reqs[mat]
        prd_cnt, srcs = consumes_counts[mat]
        if cnt > 0:
            mult = 1 + (cnt - 1) // prd_cnt
            reqs[mat] -= mult * prd_cnt
            for cnt, src_mat in srcs:
                reqs[src_mat] += mult * cnt
    return reqs


# part 1
fuel_to_ore = reduce_to_ore({**{n: 0 for n in all_nodes}, "FUEL": 1})["ORE"]
print(fuel_to_ore)

# part 2
ore_resources = 1000000000000
fuels = ore_resources // fuel_to_ore + 1
mat_reqs = reduce_to_ore({**{n: 0 for n in all_nodes}, "FUEL": fuels})
while ore_resources > mat_reqs["ORE"]:
    extra_fuel = (ore_resources - mat_reqs["ORE"]) // fuel_to_ore + 1
    fuels += extra_fuel
    mat_reqs["FUEL"] += extra_fuel
    mat_reqs = reduce_to_ore(mat_reqs)

print(fuels - 1)
