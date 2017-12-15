from days.day10 import knot_hash
from helpers import *

d = get_aoc_data(day=14)


def part1_and_2():
    start = d.data
    ct = 0

    the_map = SparseMap(default=False)
    for i in range(128):
        k = knot_hash(f'{start}-{i}')
        row = f'{int.from_bytes(k, "big"):0128b}'
        ct += row.count('1')
        the_map.add_row(i == '1' for i in row)

    label_map = defaultdict(type(None))
    equivalences = defaultdict(set)
    label_counter = count()

    for x in range(0, 128):
        for y in range(0, 128):
            if not the_map[x, y]:
                continue

            labels = {label_map[x - 1, y], label_map[x, y - 1]}
            labels.discard(None)

            mn = min(labels, default=None)
            mx = max(labels, default=None)
            if mx is not None and equivalences[mn] is not equivalences[mx]:
                label_map[x, y] = mn
                new_eqset = {*equivalences[mx], *equivalences[mn]}
                for i in new_eqset:
                    equivalences[i] = new_eqset

            elif mn is not None:
                label_map[x, y] = mn

            else:
                nl = label_map[x, y] = next(label_counter)
                equivalences[nl].add(nl)

    return ct, len(set(map(id, equivalences.values())))
