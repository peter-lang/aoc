import math

p = 20201227
s = 7
# two public keys: s_d = pow(s, d, p); s_c = pow(s, c, p)
s_d = 5764801
s_c = 17807724


def discrete_log(a, b, n):
    # https://en.wikipedia.org/wiki/Baby-step_giant-step
    # solve: pow(a, x, n) = b
    m = math.ceil(math.sqrt(n))
    log_table = dict()
    for j in range(m):
        log_table[pow(a, j, n)] = j
    a_m = pow(a, -m, n)
    for i in range(m):
        if (j := log_table.get(b, None)) is not None:
            return i * m + j
        else:
            b = b * a_m % n
    return None


d = discrete_log(7, s_d, p)
c = discrete_log(7, s_c, p)
print(pow(7, d * c, p))
