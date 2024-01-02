from functools import reduce
import operator


def parse_lines(lines):
    line_type = "rules"
    rules = dict()
    your_ticket = None
    nearby_tickets = []
    for line in lines:
        if line == "your ticket:":
            line_type = "your_ticket"
            continue
        if line == "nearby tickets:":
            line_type = "nearby_ticket"
            continue
        if line_type == "rules":
            rule_name, intervals_txt = line.split(": ")
            intervals = intervals_txt.split(" or ")
            rules[rule_name] = tuple(
                tuple(map(int, interval.split("-"))) for interval in intervals
            )
        elif line_type == "your_ticket":
            your_ticket = tuple(map(int, line.split(",")))
        elif line_type == "nearby_ticket":
            nearby_tickets.append(tuple(map(int, line.split(","))))
    return rules, your_ticket, nearby_tickets


field_rules, single_ticket, other_tickets = parse_lines(
    filter(None, map(lambda x: x.strip(), open("16.txt", "r").readlines()))
)


def invalid_field_values(ticket, rule_ranges):
    for field_value in ticket:
        if not any(
            a <= field_value <= b for rule_range in rule_ranges for a, b in rule_range
        ):
            yield field_value


def field_idx_matching(tickets, rules):
    matched_keys = dict()
    unmatched_fields = set(rules.keys())
    parking_lot = []
    unmatched_indices = set(range(len(single_ticket)))
    while unmatched_indices:
        idx = unmatched_indices.pop()
        possible_matches = []
        for key in unmatched_fields:
            if all(
                any(a <= ticket[idx] <= b for a, b in rules[key]) for ticket in tickets
            ):
                possible_matches.append(key)
        assert len(possible_matches) >= 1
        if len(possible_matches) == 1:
            field_name = possible_matches[0]
            matched_keys[field_name] = idx
            unmatched_fields.remove(field_name)
            unmatched_indices.update(parking_lot)
            parking_lot = []
        else:
            parking_lot.append(idx)
    assert not parking_lot
    return matched_keys


# part 1
print(
    sum(
        fv
        for ticket in other_tickets
        for fv in invalid_field_values(ticket, field_rules.values())
    )
)

# part 2
valid_tickets = [
    ticket
    for ticket in other_tickets
    if not list(invalid_field_values(ticket, field_rules.values()))
]

matching = field_idx_matching(valid_tickets, field_rules)
values = [single_ticket[v] for k, v in matching.items() if k.startswith("departure")]

print(reduce(operator.mul, values))
