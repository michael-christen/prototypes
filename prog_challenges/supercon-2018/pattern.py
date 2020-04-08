#!/usr/bin/env python
import itertools
from collections import defaultdict


values = [
    0x10, 0x34, 0x30, 0x12, 0x26, 0x00, 0x06, 0x07, 0x34, 0x3C, 0x10, 0x16, 0x00, 0x02, 0x14, 0x00, 0x23, 0x07, 0x3B, 0x00,
    0x30, 0x02, 0x00, 0x1F, 0x30, 0x31, 0x39, 0x30, 0x32, 0x30, 0x15, 0x00, 0x32, 0x14, 0x02, 0x00, 0x31, 0x14, 0x34,
]

mapping = {
    0x00: "_",
    0x10: "E",
    0x12: "I",
    0x26: "L",
    0x1F: "H",
    0x30: "A",
    0x31: "C",
    0x39: "K",
    0x32: "D",
    0x15: "Y",
    0x14: "O",
    0x02: "T",
    0x34: "M",
    0x7: "U",
    # GUESSES
    # 0x6: "N",
    # 0x3C: "B",
    # 0x16: "R",

}

nums = set([
    0x6,
    0x7,
    0x3C,
    0x16,
    0x23,
    0x3b,
])

"""
bumper
jumper
number
sumner
"""

remaining_letters = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ") - set(mapping.values())


def main():
    frequencies = defaultdict(int)
    for val in values:
        frequencies[val] += 1
    for val, freq in sorted(frequencies.items(), key=lambda x: x[1],
                            reverse=True):
        print hex(val), freq
    s = []
    for v in values:
        s.append(mapping.get(v, hex(v)))
    print ', '.join(s)
    print remaining_letters
    """
    for combo in itertools.permutations(remaining_letters, 4):
        word = [combo[0], combo[1], 'M', combo[2], 'E', combo[3]]
        print ''.join(word)
    """



if __name__ == '__main__':
    main()
