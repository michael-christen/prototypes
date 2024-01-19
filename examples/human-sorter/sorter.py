#!/usr/bin/env python
"""Mechanical Turk for sorting!

This is a toy to experiment with doing human in the loop sorting. Obviously
doing it with numbers is ridiculous, but this could be useful when the
comparator is inherently subjective.

Possible Future Updates:
    - Use arrow keys, and detect key presses with curses instead of requiring
    user to hit enter key
    - To make this actually useful we'd want to compare subjective items, like
    which books in a list they'd like to read.
    - We'd probably need to provide enough context for the user to compare
    these things, so we'd probably need to make a web interface that would
    display the info.

Possible Problems:
    - If there are inconsistent comparisons / the data isn't sortable then
    there should probably be some way of alerting that.
"""
import time


def compare(a, b):
    msg = "{} or {}".format(a, b)
    val = raw_input(msg)
    if val == '<':
        return 1
    elif val == '>':
        return -1
    else:
        return 0


def main():
    list_of_numbers = [
        0,
        20,
        10
    ]
    human_start = time.time()
    human_sorted = sorted(list_of_numbers, cmp=compare)
    human_time = time.time() - human_start

    cpu_start = time.time()
    typical_sorted = sorted(list_of_numbers)
    cpu_time = time.time() - cpu_start
    assert human_sorted == typical_sorted, (
        "yours: {}\nright: {}".format(human_sorted, typical_sorted))
    print("Nice sorting! You matched the computer. It took you {:.2f} seconds "
          "and it took the computer {:.2E} seconds, so you were {:.2f} times "
          "slower, but that's ok.".format(
              human_time, cpu_time, human_time / cpu_time))


if __name__ == '__main__':
    main()

