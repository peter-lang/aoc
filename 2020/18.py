import re
from abc import ABC, abstractmethod

lines = list(filter(None, map(lambda x: x.strip(), open("18.txt", "r").readlines())))


def memoize(func):
    def memoize_wrapper(self, *args):
        pos = self.position
        memo = self.memos.get(pos)
        if memo is None:
            memo = self.memos[pos] = {}
        key = (func, args)
        if key in memo:
            res, end_pos = memo[key]
            self.position = end_pos
        else:
            res = func(self, *args)
            end_pos = self.position
            if res:
                assert end_pos > pos
            else:
                assert end_pos == pos
            memo[key] = res, end_pos
        return res

    return memoize_wrapper


def memoize_left_rec(func):
    def memoize_left_rec_wrapper(self, *args):
        pos = self.position
        memo = self.memos.get(pos)
        if memo is None:
            memo = self.memos[pos] = {}
        key = (func, args)
        if key in memo:
            res, end_pos = memo[key]
            self.position = end_pos
        else:
            memo[key] = last_res, last_pos = None, pos

            # Loop until no longer parse is obtained.
            while True:
                self.position = pos
                res = func(self, *args)
                end_pos = self.position
                if end_pos <= last_pos:
                    break
                memo[key] = last_res, last_pos = res, end_pos

            res = last_res
            self.position = last_pos
        return res

    return memoize_left_rec_wrapper


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


class FunctionNode:
    def __init__(self, operation, children):
        self.operation = operation
        self.children = children

    def __call__(self):
        return self.operation(*(child() for child in self.children))


class AbstractParser(ABC):
    def __init__(self):
        self.input = None
        self.position = None
        self.memos = None
        self.integer_pattern = re.compile("^\\s*(?P<value>[0-9]+)\\s*")

    def parse(self, input):
        self.input = input
        self.position = 0
        self.memos = dict()
        result = self.expr()
        if self.position == len(input):
            return result
        return None

    @memoize
    def integer(self):
        pos = self.position
        match = self.integer_pattern.match(self.input[pos:])
        if match:
            self.position = pos + match.end()
            return NumberNode(int(match.group("value")))
        return None

    @memoize
    def expect(self, code):
        pos = self.position
        while pos + 1 <= len(self.input) and self.input[pos].isspace():
            pos += 1

        if (
            pos + len(code) <= len(self.input)
            and self.input[pos : (pos + len(code))] == code
        ):
            pos += len(code)
            while pos + 1 <= len(self.input) and self.input[pos].isspace():
                pos += 1
            self.position = pos
            return True
        return False

    @memoize
    def atom(self):
        pos = self.position
        if num := self.integer():
            return num
        self.position = pos
        if self.expect("(") and (expr := self.expr()) and self.expect(")"):
            return expr
        self.position = pos
        return None

    @abstractmethod
    def expr(self):
        pass


class SamePrecedence(AbstractParser):
    def __init__(self):
        super().__init__()

    @memoize_left_rec
    def expr(self):
        pos = self.position
        if (lhs := self.expr()) and self.expect("*") and (rhs := self.atom()):
            return FunctionNode(lambda a, b: a * b, [lhs, rhs])
        self.position = pos
        if (lhs := self.expr()) and self.expect("+") and (rhs := self.atom()):
            return FunctionNode(lambda a, b: a + b, [lhs, rhs])
        self.position = pos
        if atom := self.atom():
            return atom
        self.position = pos
        return None


class SwappedPrecedence(AbstractParser):
    def __init__(self):
        super().__init__()

    @memoize_left_rec
    def term(self):
        pos = self.position
        if (lhs := self.term()) and self.expect("+") and (rhs := self.atom()):
            return FunctionNode(lambda a, b: a + b, [lhs, rhs])
        if atom := self.atom():
            return atom
        self.position = pos
        return None

    @memoize_left_rec
    def expr(self):
        pos = self.position
        if (lhs := self.expr()) and self.expect("*") and (rhs := self.term()):
            return FunctionNode(lambda a, b: a * b, [lhs, rhs])
        self.position = pos
        if term := self.term():
            return term
        self.position = pos
        return None


# part 1
p = SamePrecedence()
print(sum(p.parse(line)() for line in lines))

# part 2
p = SwappedPrecedence()
print(sum(p.parse(line)() for line in lines))
