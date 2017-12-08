from helpers import *

d = get_aoc_data(day=8)


def part1_and_2():
    regs = defaultdict(int)
    absolute_maximum = 0
    for target, op, val, cond, op2, val2 in d.parsed(
            '<> <str:inc|dec> <int> if <> <> <int>'):
        # __builtins__ gets injected here, so make a copy
        if eval(f'{cond} {op2} {val2}', defaultdict(int, regs)):
            if op == 'inc':
                regs[target] += val
            else:
                assert op == 'dec'
                regs[target] -= val

            absolute_maximum = max(max(regs.values()), absolute_maximum)

    return max(regs.values()), absolute_maximum
