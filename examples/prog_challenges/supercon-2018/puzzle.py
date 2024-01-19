#!/usr/bin/env python


DIGITS = set([
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
])



"""
def solve_puzzle():
    position = (
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
    )
    solution = []
    solution_number = 0
    available_digits = set()
    position = 1
    while len(solution) < len(digits):
        chosen_digit = None
        for d in DIGITS:
            if d not in available_digits:
                continue
            if (solution_number + d) % i == 0:
                chosen_digit = d
                # TODO: recurse
"""


def get_number(solution_list):
    num = 0
    for i, elt in enumerate(reversed(solution_list)):
        num += pow(10, i) * elt
    return num


def get_digits(num):
    l = []
    while num > 0:
        l += num % 10
        num = num / 10
    return l


def solve(used_digits):
    solution = get_number(used_digits)
    print solution
    available_digits = DIGITS - set(used_digits)
    if len(available_digits) == 0:
        return solution
    level = len(used_digits) + 1
    for d in available_digits:
        print d
        new_solution = solution * 10 + d
        if new_solution % level == 0:
            possible_solution = solve(used_digits + [d])
            if possible_solution is not None:
                return possible_solution
    return None


def main():
    print solve([])


if __name__ == '__main__':
    main()

