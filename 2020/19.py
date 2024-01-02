from itertools import product

lines = map(lambda x: x.strip(), open("19.txt", "r").readlines())
parse_rules = True
ALL_RULES = dict()
WORDS = []
for line in lines:
    if not line:
        parse_rules = False
        continue
    if parse_rules:
        name, body = line.split(": ")
        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]
            assert len(body) == 1
            rule = body
        else:
            rule = [
                list(map(int, alt_rule.split(" "))) for alt_rule in body.split(" | ")
            ]
        ALL_RULES[int(name)] = rule
    else:
        WORDS.append(line)


def all_joined(rules_dict, seq_rule):
    for res in product(*(generate_valid_words(rules_dict, r) for r in seq_rule)):
        yield "".join(res)


def generate_valid_words(rules_dict, rule_name) -> set[str]:
    alt_rules = rules_dict[rule_name]
    if isinstance(alt_rules, str):
        return {alt_rules}
    else:
        return set(
            word for seq_rule in alt_rules for word in all_joined(rules_dict, seq_rule)
        )


rule_42 = generate_valid_words(ALL_RULES, 42)
rule_31 = generate_valid_words(ALL_RULES, 31)

r_len = len(next(iter(rule_42)))
assert all(len(r) == r_len for r in rule_42)
assert all(len(r) == r_len for r in rule_31)
assert len(rule_31 & rule_42) == 0


# part 1
def is_valid_1(txt):
    # original:
    # 0: 8 11
    # 8: 42
    # 11: 42 31
    if len(txt) != 3 * r_len:
        return False
    return (
        txt[0:r_len] in rule_42
        and txt[r_len : (2 * r_len)] in rule_42
        and txt[(2 * r_len) : (3 * r_len)] in rule_31
    )


print(sum(is_valid_1(w) for w in WORDS))


# part 2
def is_valid_2(txt):
    # modified:
    # 0: 8 11
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    rule_31_cnt = 0
    while txt[-r_len:] in rule_31:
        rule_31_cnt += 1
        txt = txt[:-r_len]

    rule_42_cnt = 0
    while txt[-r_len:] in rule_42:
        rule_42_cnt += 1
        txt = txt[:-r_len]

    return len(txt) == 0 and 0 < rule_31_cnt < rule_42_cnt


print(sum(is_valid_2(w) for w in WORDS))
