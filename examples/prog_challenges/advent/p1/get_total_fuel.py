import sys

def compute_fuel(mass: int) -> int:
    return mass // 3 - 2


def get_total_fuel(mass: int) -> int:
    additional = compute_fuel(mass)
    if additional <= 0:
        return 0
    else:
        return additional + get_total_fuel(additional)

def main():
    total = 0
    for l in sys.stdin.readlines():
        l = l.strip()
        if not l:
            continue
        total += get_total_fuel(int(l))
    print(total)


if __name__ == '__main__':
    main()

