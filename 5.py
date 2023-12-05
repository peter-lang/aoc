from bisect import bisect_right, insort_right
from itertools import islice

lines: list[str] = list(
    filter(None, map(lambda x: x.strip(), open("5.txt", "r").readlines()))
)

seeds = []
mappings = []
for l in lines:
    if l.startswith("seeds:"):
        seeds = list(map(lambda x: int(x.strip()), l[len("seeds:") :].split()))
    elif l.endswith("map:"):
        mappings.append([])
    else:
        _dst, _src, _len = list(map(lambda x: int(x.strip()), l.split()))
        insort_right(mappings[-1], (_src, _len, _dst))


# part 1
def map_seed_to_location(s):
    for m in mappings:
        idx = bisect_right(m, (s + 1,))
        if idx == 0:
            continue
        src, m_len, dst = m[idx - 1]
        if s < src or s >= src + m_len:
            continue
        s = s - src + dst
    return s


print(min(map_seed_to_location(seed) for seed in seeds))


# part 2
def map_seed_range_to_location(src_ranges):
    for m in mappings:
        dst_ranges = []
        for range_start, remaining_range_len in src_ranges:
            while remaining_range_len > 0:
                # src_range:      |-----------|
                # map_range: |idx-1....|   |idx......|
                idx = bisect_right(m, (range_start + 1,))
                if idx < len(m):
                    # src_range:      |-----------|
                    # map_range: |idx-1....|   |idx......|
                    # select   :      |========|--|
                    m_src_next, _, _ = m[idx]
                    range_len = min(remaining_range_len, m_src_next - range_start)
                else:
                    # src_range:      |-----------|
                    # map_range: |idx(-1)..|
                    # select   :      |===========|
                    range_len = remaining_range_len

                if idx == 0:
                    # src_range:    |--------|
                    # map_range:             |idx(0)...|
                    # select   :    |========|
                    dst_ranges.append((range_start, range_len))
                else:
                    m_src, m_len, m_dst = m[idx - 1]
                    mapped_len = max(0, min(m_src - range_start + m_len, range_len))
                    unmapped_len = range_len - mapped_len
                    if mapped_len:
                        # src_range:      |--------|
                        # map_range: |idx-1....|
                        # select   :      |====|...|
                        dst_ranges.append((range_start - m_src + m_dst, mapped_len))
                    if unmapped_len:
                        # src_range:      |--------|
                        # map_range: |idx-1....|
                        # select   :      |....|===|
                        dst_ranges.append((range_start + mapped_len, unmapped_len))
                range_start += range_len
                remaining_range_len -= range_len
        src_ranges = dst_ranges
    return src_ranges


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = tuple(islice(it, n))
        if not batch:
            return
        yield batch


print(min(map_seed_range_to_location(list(batched(seeds, 2))))[0])
