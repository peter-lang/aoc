from typing import NamedTuple, Optional
import re
from functools import cache

Condition = NamedTuple("Condition", (("prop", str), ("op", str), ("val", int)))
SubRule = tuple[Optional[Condition], str]
Value = NamedTuple("Value", (("x", int), ("m", int), ("a", int), ("s", int)))
ValueRange = NamedTuple(
    "Value",
    (
        ("x", tuple[int, int]),
        ("m", tuple[int, int]),
        ("a", tuple[int, int]),
        ("s", tuple[int, int]),
    ),
)
Rule = NamedTuple("Rule", (("name", str), ("rules", list[SubRule])))

rule_pattern = re.compile(r"(\S+)\{([^}]+)\}")
value_pattern = re.compile(r"\{([^}]+)\}")


def tokenize(s: str, tokens: list[str]):
    result = [s]
    for t in tokens:
        tmp = []
        for part in result:
            sub_parts = part.split(t)
            tmp.append(sub_parts[0])
            for sp in sub_parts[1:]:
                tmp.append(t)
                tmp.append(sp)
        result = tmp
    return result


def parse_value(s: str) -> Value:
    m = value_pattern.match(s)
    body = m.group(1)
    return Value(**{k: int(v) for k, v in (kv.split("=") for kv in body.split(","))})


def parse_rule(s: str) -> Rule:
    m = rule_pattern.match(s)
    name = m.group(1)
    body = m.group(2)
    rules: list[SubRule] = []
    for sr in body.split(","):
        sr_parts = sr.split(":")
        if len(sr_parts) == 1:
            rules.append((None, sr_parts[0]))
        else:
            cond = tokenize(sr_parts[0], ["<", ">"])
            rules.append(
                (Condition(prop=cond[0], op=cond[1], val=int(cond[2])), sr_parts[1])
            )
    return Rule(name=name, rules=rules)


RULES = dict()
VALUES = []
parsing_rules = True
for line in map(lambda x: x.strip(), open("19.txt", "r").readlines()):
    if not line:
        parsing_rules = False
        continue
    if parsing_rules:
        parsed = parse_rule(line)
        RULES[parsed.name] = parsed
    else:
        parsed = parse_value(line)
        VALUES.append(parsed)


def eval_condition(c: Condition, v: Value) -> bool:
    if c.op == ">":
        return getattr(v, c.prop) > c.val
    elif c.op == "<":
        return getattr(v, c.prop) < c.val


def execute_rule(rule_name: str, value: Value) -> bool:
    rule = RULES[rule_name]
    for condition, dst in rule.rules:
        if condition is None or eval_condition(condition, value):
            if dst in ("R", "A"):
                return dst == "A"
            else:
                return execute_rule(dst, value)


def sum_ratings(v: Value) -> int:
    return v.x + v.m + v.a + v.s


# part 1
print(sum(sum_ratings(f) for f in filter(lambda v: execute_rule("in", v), VALUES)))


DEFAULT_VALUE_RANGE = ValueRange(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000))


def intersect(lhs: ValueRange, rhs: ValueRange):
    return ValueRange(
        x=(max(lhs.x[0], rhs.x[0]), min(lhs.x[1], rhs.x[1])),
        m=(max(lhs.m[0], rhs.m[0]), min(lhs.m[1], rhs.m[1])),
        a=(max(lhs.a[0], rhs.a[0]), min(lhs.a[1], rhs.a[1])),
        s=(max(lhs.s[0], rhs.s[0]), min(lhs.s[1], rhs.s[1])),
    )


def is_empty(vr: ValueRange) -> bool:
    return any(b < a for a, b in (getattr(vr, p) for p in ("x", "m", "a", "s")))


def split(c: Condition, vr: ValueRange):
    unchanged = {p: getattr(vr, p) for p in ("x", "m", "a", "s") if p != c.prop}
    p_min, p_max = getattr(vr, c.prop)
    if c.op == ">":
        return (
            ValueRange(**{**unchanged, c.prop: (max(p_min, c.val + 1), p_max)}),
            ValueRange(**{**unchanged, c.prop: (p_min, min(p_max, c.val))}),
        )
    elif c.op == "<":
        return (
            ValueRange(**{**unchanged, c.prop: (p_min, min(p_max, c.val - 1))}),
            ValueRange(**{**unchanged, c.prop: (max(p_min, c.val), p_max)}),
        )


@cache
def accepted_value_ranges(rule_name: str) -> list[ValueRange]:
    rule = RULES[rule_name]
    accepted = []
    vr = DEFAULT_VALUE_RANGE
    for condition, dst in rule.rules:
        if condition is None:
            vr_cond = vr
        else:
            vr_cond, vr = split(condition, vr)

        if dst == "A":
            accepted.append(vr_cond)
        elif dst != "R":
            for vr_dst in accepted_value_ranges(dst):
                vr_dst = intersect(vr_cond, vr_dst)
                if not is_empty(vr_dst):
                    accepted.append(vr_dst)
    return accepted


def vr_size(vr: ValueRange) -> int:
    def range_size(r: tuple[int, int]):
        return r[1] - r[0] + 1

    return range_size(vr.x) * range_size(vr.m) * range_size(vr.a) * range_size(vr.s)


print(sum(vr_size(vr) for vr in accepted_value_ranges("in")))
