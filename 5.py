from bisect import bisect_right, insort_right
from itertools import islice
from typing import Sequence

lines: list[str] = list(filter(None, map(lambda x: x.strip(), open("5.txt", "r").readlines())))

seeds = []
mappings = []
for l in lines:
    if l.startswith("seeds:"):
        seeds = list(map(lambda x: int(x.strip()), l[len("seeds:"):].split()))
    elif l.endswith("map:"):
        mappings.append([])
    else:
        _dst, _src, _len = list(map(lambda x: int(x.strip()), l.split()))
        insort_right(mappings[-1], (_src, _len, _dst))


# part 1
def map_seed_to_location(s):
    for m in mappings:
        pos = bisect_right(m, (s + 1,))
        if pos == 0:
            continue
        src, m_len, dst = m[pos - 1]
        if s < src or s >= src + m_len:
            continue
        s = s - src + dst
    return s


print(min(map_seed_to_location(seed) for seed in seeds))


# part 2
class IndexedRange(Sequence):
    def __init__(self, start, length):
        self.start = start
        self.length = length

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.start + idx


def map_seed_range_to_location(src_ranges):
    def find_first_mapped_range(_m, s, max_len):
        p = bisect_right(_m, (s + 1,))
        # find last index which would have the same mapping
        p_len = bisect_right(IndexedRange(s, max_len), p, key=lambda x: bisect_right(_m, (x + 1,)))
        return p, p_len

    for m in mappings:
        dst_ranges = []
        for range_start, remaining_range_len in src_ranges:
            while remaining_range_len > 0:
                # cut src_ranges by map_ranges starts:
                # src_ranges: |-----|  |----------|   |---|
                # map_ranges:     |-------|     |---|
                # cut ranges: |---|-|  |--------|-|   |---|
                # select first, along with the last mapped_range, that starts at the same point or before
                idx, range_len = find_first_mapped_range(m, range_start, remaining_range_len)
                if idx == 0:
                    # src_range is before all existing mapping
                    dst_ranges.append((range_start, range_len))
                else:
                    m_src, m_len, m_dst = m[idx - 1]
                    if range_start >= m_src + m_len:
                        # src_range:         |---|
                        # map_range: |----|
                        dst_ranges.append((range_start, range_len))
                    else:
                        # src_range: |-----.....|
                        # map_range: |-----|
                        mapped_len = min(m_src - range_start + m_len, range_len)
                        unmapped_len = range_len - mapped_len
                        dst_ranges.append((range_start - m_src + m_dst, mapped_len))
                        if unmapped_len:
                            # src_range: |.....-----|
                            # map_range: |-----|
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
