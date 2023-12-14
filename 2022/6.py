text = open("6.txt", "r").read()


def first_n_different_chars(txt, n):
    for i in range(n, len(txt)):
        if len(set(txt[(i - n) : i])) == n:
            return i


# part 1
print(first_n_different_chars(text, 4))

# part 2
print(first_n_different_chars(text, 14))
