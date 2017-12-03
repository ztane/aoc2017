#!/usr/bin/env python3
import sys
import time
from datetime import datetime

if sys.version_info < (3,):
    print('WTF, are you running my code in Python 2??!')
    sys.exit(1)

if __name__ == '__main__':
    day = int(sys.argv[1])
    if len(sys.argv) != 2:
        print('Usage: runner.py daynumber')
        sys.exit(2)

    while True:
        now = datetime.now()
        if day <= now.day:
            break

        print('Time has not yet come, current UTC time is {}'.format(now),
              end='\r')
        time.sleep(1)

    day_module = 'day{:02}'.format(day)
    module = getattr(__import__('days.' + day_module), day_module)
    for part in [1, 2]:
        func = getattr(module, 'part{}'.format(part), None)
        if func:
            print('Day {} part {}'.format(day, part))
            val = func()
            print(val)
        else:
            print('Day {}; no part {}'.format(day, part))
