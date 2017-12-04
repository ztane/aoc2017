from itertools import combinations

from helpers import get_aoc_data

d = get_aoc_data(day=4)


def part1():
    return sum(len(phrase) == len(set(phrase)) for phrase in d.sentences)


def part2():
    return sum(
        all(sorted(w1) != sorted(w2) for w1, w2 in combinations(phrase, 2))
        for phrase in d.sentences
    )
