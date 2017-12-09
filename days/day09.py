from helpers import *

d = get_aoc_data(day=9)


def part1_and_2():
    open_groups = []
    total_score = 0
    garbage = False
    ignore = False
    garbage_score = 0
    for i in d.data:
        if ignore:
            ignore = False
            continue

        if i == '!':
            ignore = True
            continue

        if not garbage:
            if i == '{':
                open_groups.append(1)
            if i == '}':
                total_score += len(open_groups)
                open_groups.pop()
            if i == '<':
                garbage = True
                continue

        else:
            if i == '>':
                garbage = False

        if garbage:
            garbage_score += 1

    return total_score, garbage_score
