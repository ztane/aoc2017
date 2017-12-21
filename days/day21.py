import numpy

from helpers import get_aoc_data

d = get_aoc_data(day=21)
rules = {}


def parse_rule(line):
    return numpy.array([
        [cell == '#' for cell in row]
        for row in
        line.split('/')
    ])


def expand(state):
    rule_size = [2, 3][len(state) % 2]
    total = []
    tile_range = range(0, len(state), rule_size)
    for y in tile_range:
        row = []
        for x in tile_range:
            row.append(
                rules[state[y: y + rule_size, x: x + rule_size].tobytes()])

        total.append(row)

    return numpy.block(total)


def part1_and_2():
    state = numpy.array(
        [[0, 1, 0],
         [0, 0, 1],
         [1, 1, 1]],
        dtype=bool
    )

    for src, tgt in d.parsed('<> => <>'):
        src = parse_rule(src)
        tgt = parse_rule(tgt)
        for transposed in [src, src.T]:
            for y_flip in [transposed, numpy.flipud(transposed)]:
                for x_flip in [y_flip, numpy.fliplr(y_flip)]:
                    rules[x_flip.tobytes()] = tgt

    for i in range(18):
        if i == 5:
            part1 = numpy.count_nonzero(state)
        state = expand(state)

    return part1, numpy.count_nonzero(state)

