import numpy as np

last_tile_no = None
tile_lines = []
tiles = dict()
for line in filter(None, map(lambda x: x.strip(), open("20.txt", "r").readlines())):
    if line.startswith("Tile "):
        if last_tile_no is not None and tile_lines:
            tiles[last_tile_no] = np.array(
                [[ch == "#" for ch in tl] for tl in tile_lines], dtype=np.uint8
            )
            tile_lines = []
        last_tile_no = int(line[5:-1])
    else:
        tile_lines.append(line)
if last_tile_no is not None and tile_lines:
    tiles[last_tile_no] = np.array(
        [[ch == "#" for ch in tl] for tl in tile_lines], dtype=np.uint8
    )

FIRST_KEY = next(iter(tiles.keys()))
TILE_SHAPE = tiles[FIRST_KEY].shape
assert all(t.shape == TILE_SHAPE for t in tiles.values())


#
def fits(a, b, relative_coord):
    # r-c
    if relative_coord[0] == 1:
        # orientation: a
        #              b
        return np.all(a[-1, :] == b[0, :])
    elif relative_coord[0] == -1:
        # orientation: b
        #              a
        return np.all(b[-1, :] == a[0, :])
    elif relative_coord[1] == -1:
        # orientation: ba
        return np.all(b[:, -1] == a[:, 0])
    elif relative_coord[1] == 1:
        # orientation: ab
        return np.all(a[:, -1] == b[:, 0])


def all_orientations(tile):
    r = tile
    yield r
    yield np.flip(r, 0)
    r = np.rot90(r)
    yield r
    yield np.flip(r, 0)
    r = np.rot90(r)
    yield r
    yield np.flip(r, 0)
    r = np.rot90(r)
    yield r
    yield np.flip(r, 0)


def yield_neighbours(c):
    yield c[0] + 1, c[1]
    yield c[0] - 1, c[1]
    yield c[0], c[1] + 1
    yield c[0], c[1] - 1


def try_add_tile(tiles_by_coord, edges, tile_id):
    for e, neighbours in edges.items():
        for oriented_tile in all_orientations(tiles[tile_id]):
            if all(
                fits(oriented_tile, tiles_by_coord[n][1], (n[0] - e[0], n[1] - e[1]))
                for n in neighbours
            ):
                tiles_by_coord[e] = (tile_id, oriented_tile)
                del edges[e]
                for new_edge in yield_neighbours(e):
                    if new_edge in edges:
                        edges[new_edge].append(e)
                    else:
                        edges[new_edge] = [e]
                return True
    return False


def align_tiles(start):
    unmatched_tiles = list(k for k in tiles.keys() if k != start)
    matched_tiles = {(0, 0): (start, tiles[start])}
    edges = {p: [(0, 0)] for p in yield_neighbours((0, 0))}
    while unmatched_tiles:
        unmatched_len = len(unmatched_tiles)
        found = False
        for idx in range(unmatched_len):
            selected_id = unmatched_tiles[idx]
            if try_add_tile(matched_tiles, edges, selected_id):
                unmatched_tiles = unmatched_tiles[:idx] + unmatched_tiles[(idx + 1) :]
                found = True
                break
        assert found
    return matched_tiles


aligned_tiles = align_tiles(FIRST_KEY)

coords = list(aligned_tiles.keys())
x_min, x_max = min(c[0] for c in coords), max(c[0] for c in coords)
y_min, y_max = min(c[1] for c in coords), max(c[1] for c in coords)

# part 1
corner_product = (
    aligned_tiles[(x_min, y_min)][0]
    * aligned_tiles[(x_max, y_min)][0]
    * aligned_tiles[(x_min, y_max)][0]
    * aligned_tiles[(x_max, y_max)][0]
)
print(corner_product)


monster = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    ],
    np.uint8,
)


def find_image(a, img):
    expected = img.sum()
    for x in range(a.shape[0] - img.shape[0] + 1):
        for y in range(a.shape[1] - img.shape[1] + 1):
            masked = a[x : (x + img.shape[0]), y : (y + img.shape[1])] * img
            if masked.sum() == expected:
                yield x, y


merged_shape = (
    (TILE_SHAPE[0] - 2) * (x_max - x_min + 1),
    (TILE_SHAPE[1] - 2) * (y_max - y_min + 1),
)
merged = np.zeros(merged_shape, dtype=np.uint8)
for x in range(x_min, x_max + 1):
    x_slice = slice(
        (TILE_SHAPE[0] - 2) * (x - x_min), (TILE_SHAPE[0] - 2) * (x - x_min + 1)
    )
    for y in range(y_min, y_max + 1):
        y_slice = slice(
            (TILE_SHAPE[1] - 2) * (y - y_min), (TILE_SHAPE[1] - 2) * (y - y_min + 1)
        )
        merged[x_slice, y_slice] = aligned_tiles[(x, y)][1][1:-1, 1:-1]


mon_locs = np.zeros(merged_shape, dtype=np.uint8)
for mon_ori in all_orientations(monster):
    for loc in find_image(merged, mon_ori):
        x_slice = slice(loc[0], loc[0] + mon_ori.shape[0])
        y_slice = slice(loc[1], loc[1] + mon_ori.shape[1])
        mon_locs[x_slice, y_slice] = np.maximum(mon_ori, mon_locs[x_slice, y_slice])

# part 2
print((merged - mon_locs).sum())
