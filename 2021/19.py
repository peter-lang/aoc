import numpy as np

scanners = []
for line in filter(None, map(lambda x: x.strip(), open("19.txt", "r").readlines())):
    if line.startswith("--- scanner"):
        scanners.append([])
    else:
        scanners[-1].append(np.array(list(map(int, line.split(",")))))


x_rots = [
    # 0
    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    # 90
    np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
    # 180
    np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]),
    # 270
    np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
]

y_rots = [
    # 0
    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    # 90
    np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
    # 180
    np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]),
    # 270
    np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
]

z_rots = [
    # 0
    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    # 90
    np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
    # 180
    np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
    # 270
    np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
]


def all_3d_rots():
    result = []
    for x_idx in range(4):
        for y_idx in range(4):
            for z_idx in range(4):
                rot = x_rots[x_idx] @ y_rots[y_idx] @ z_rots[z_idx]
                if any(np.all(r == rot) for r in result):
                    continue
                result.append(rot)
    return result


all_rots = all_3d_rots()
assert len(all_rots) == 24


def aligned_pts(base_aligned_pts, search_pts, min_common):
    for base_pt in base_aligned_pts:
        base_pts_norm = set(tuple(pt - base_pt) for pt in base_aligned_pts)
        for rot in all_rots:
            search_pts_rot = [rot @ search_pt for search_pt in search_pts]
            for search_pt_rot in search_pts_rot:
                sorch_pts_rot_norm = set(
                    tuple(pt - search_pt_rot) for pt in search_pts_rot
                )
                if len(base_pts_norm & sorch_pts_rot_norm) >= min_common:
                    aligned_beacons = [
                        pt - search_pt_rot + base_pt for pt in search_pts_rot
                    ]
                    search_origin = base_pt - search_pt_rot
                    return aligned_beacons, search_origin
    return None


open_set = {0}
aligned = {0: (scanners[0], np.array([0, 0, 0]))}
visited = set()
while len(aligned) < len(scanners) and open_set:
    base_idx = open_set.pop()
    for search_idx in range(len(scanners)):
        if base_idx == search_idx or search_idx in aligned:
            continue
        edge = frozenset([search_idx, base_idx])
        if edge in visited:
            continue
        visited.add(edge)
        res = aligned_pts(aligned[base_idx][0], scanners[search_idx], 12)
        if res is not None:
            aligned[search_idx] = res
            open_set.add(search_idx)

# part 1
all_beacons = set(
    tuple(beacon) for beacons, _ in aligned.values() for beacon in beacons
)
print(len(all_beacons))

# part 2
all_sensors = [sensor for _, sensor in aligned.values()]
print(
    max(
        np.abs(s1 - s2).sum()
        for s1_idx, s1 in enumerate(all_sensors)
        for s2 in all_sensors[:s1_idx]
    )
)
