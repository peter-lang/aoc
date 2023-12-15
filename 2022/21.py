from typing import NamedTuple, Union
import operator
import sympy

Symbol = NamedTuple('Symbol', [('op', str), ('a', str), ('b', str)])

VALUE = Union[Symbol, int]

OPERATOR = {
    '*': operator.mul,
    '/': operator.floordiv,
    '+': operator.add,
    '-': operator.sub
}

def parse(s: str) -> VALUE:
    if s.isdigit():
        return int(s)
    else:
        a, op, b = s.split()
        return Symbol(op, a, b)


def eval_int(value: VALUE, decode: dict[str, VALUE]) -> int:
    if isinstance(value, int):
        return value
    else:
        return OPERATOR[value.op](eval_int(decode[value.a], decode), eval_int(decode[value.b], decode))


monkeys = {
    k.strip(): parse(v.strip())
    for k, v in
    (line.split(":") for line in filter(None, map(lambda x: x.strip(), open("21.txt", "r").readlines())))
}

# part 1
print(int(eval_int(monkeys["root"], monkeys)))


def eval_str(name: str, decode: dict[str, VALUE]):
    if name == "humn":
        return 'x'
    v = decode[name]
    if isinstance(v, int):
        return str(v)
    else:
        return f"({eval_str(v.a, decode)}{v.op}{eval_str(v.b, decode)})"


# part 2
root = monkeys["root"]
lhs = eval_str(root.a, monkeys)
rhs = eval_str(root.b, monkeys)
equation = f"({lhs})-({rhs})"
expr = sympy.sympify(equation)
result = sympy.solve(expr)
print(result[0])
