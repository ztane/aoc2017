from helpers import *

d = get_aoc_data(day=6)


def part1_and_2():
    memory = ring_list(d.extract_ints)
    seen = counting_set([tuple(memory)])
    get_second = op.itemgetter(1)

    for step in count(1):
        cell, value = max(enumerate(memory), key=get_second)
        memory[cell] = 0

        for i in range(1, value + 1):
            memory[cell + i] += 1

        state = tuple(memory)
        if state in seen:
            cycle_start = seen[state]
            return step, step - cycle_start + 1

        seen.add(state)
