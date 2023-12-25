from collections import Counter


def parse_policy(p):
    ran, ch = p.split(" ")
    a, b = ran.split("-")
    return int(a), int(b), ch


policy_pwds = [
    (parse_policy(pol), pwd)
    for pol, pwd in map(
        lambda x: x.split(": "),
        filter(None, map(lambda x: x.strip(), open("2.txt", "r").readlines())),
    )
]


def is_valid_1(pol_pwd):
    pol, pwd = pol_pwd
    a, b, ch = pol
    cnt = Counter(pwd)[ch]
    return a <= cnt <= b


def is_valid_2(pol_pwd):
    pol, pwd = pol_pwd
    a, b, ch = pol
    return (
        pwd[a - 1] == ch and pwd[b - 1] != ch or pwd[a - 1] != ch and pwd[b - 1] == ch
    )


# part 1
print(len(list(filter(is_valid_1, policy_pwds))))

# part 2
print(len(list(filter(is_valid_2, policy_pwds))))
