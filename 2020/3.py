lines = list(filter(None, map(lambda x: x.strip(), open("3.txt", "r").readlines())))

def tree_count(d_x, d_y):
    x, y = d_x, d_y
    cnt = 0
    while x < len(lines):
        if lines[x][y%len(lines[x])] == '#':
            cnt += 1
        x += d_x
        y += d_y
    return cnt

# part 1
print(tree_count(1, 3))

# part 2
print(tree_count(1, 1) * tree_count(1, 3) * tree_count(1, 5) * tree_count(1, 7) * tree_count(2, 1))
