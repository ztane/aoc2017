Advent of Code 2017
===================

As solved by Antti Haapala
--------------------------

In 2015 I did pretty well in Advent of Code until the last puzzle.
The last puzzle proved to be a bit tricky because of lack of coffee - the 
puzzles were released at 7 AM local time, and I couldn't get up early enough
on the Christmas Day and thus wasn't ranked among final top 100.

In 2016 I tried to be a bit smarter and tried to reduce the amount of boilerplate
code - I had made a runner executable and a helper module that contains 
some shortcuts, including reading the input in various ways, so that instead of

:: 

    with open('input') as f:
        for i in f.strip().split(', '):
            

I can directly use

::

    for i in input_split():

The helpers also imports the contents of ``collections``, ``itertools``, ``functools``
and ``math`` so that their contents can be used without prologue.

Finally I had written some useful functions such as ``clamp`` to force a value to be 
within minimum and maximum.

This year (2017) I will continue solving AOC and developing the module in the hopes
that I might secure a better place on the scoreboard.

Running the solutions
---------------------

Simply use ``AOC_SESSION=deadbeefyoursessionkey python3 runner.py daynumber``.
