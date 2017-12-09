from helpers import *

d = get_aoc_data(day=9)


def part1_and_2():
    open_groups = 0
    total_score = garbage_score = 0
    garbage = ignore = False
    for i in d.data:
        if ignore:
            ignore = False

        elif i == '!':
            ignore = True

        elif garbage:
            if i == '>':
                garbage = False
            else:
                garbage_score += 1

        else:
            if i == '{':
                open_groups += 1

            if i == '}':
                total_score += open_groups
                open_groups -= 1

            if i == '<':
                garbage = True

    return total_score, garbage_score
