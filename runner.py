#!/usr/bin/env python3
import sys
import time
from datetime import datetime, timezone

if sys.version_info < (3,):
    print('WTF, are you running my code in Python 2??!')
    sys.exit(1)

if __name__ == '__main__':
    day = int(sys.argv[1])
    if len(sys.argv) != 2:
        print('Usage: runner.py daynumber')
        sys.exit(2)

    waiting = False
    while True:
        target = datetime(2017, 12, day, 5, 0, tzinfo=timezone.utc)
        now = datetime.now(tz=timezone.utc).replace(microsecond=0)
        if target < now:
            break

        print('\rCurrent UTC time is {}; waiting for {}    '
              .format(str(now).replace('+00:00', ''), target - now), end='')
        time.sleep(1)
        waiting = True

    if waiting:
        print('\nWaiting two extra seconds, just to be sure')
        time.sleep(2)

    day_module = 'day{:02}'.format(day)
    module = getattr(__import__('days.' + day_module), day_module)
    both_parts = getattr(module, 'part1_and_2', None)
    if both_parts:
        part1, part2 = both_parts()
        print('Day {} part 1\n{}'.format(day, part1))
        print('Day {} part 2\n{}'.format(day, part2))

    else:
        for part in [1, 2]:
            func = getattr(module, 'part{}'.format(part), None)
            if func:
                print('Day {} part {}'.format(day, part))
                val = func()
                print(val)
            else:
                print('Day {}; no part {}'.format(day, part))
