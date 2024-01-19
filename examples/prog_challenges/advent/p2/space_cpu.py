import sys

from collections import defaultdict

from tqdm import tqdm

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt


def run_program(line: str) -> str:
    memory = defaultdict(int)
    data = list(map(int, line.split(',')))
    for i, v in enumerate(data):
        memory[i] = v
    i = 0
    while True:
        opcode = memory[i]
        if opcode == 99:
            break
        elif opcode == 1:
            f = lambda a, b: a + b
        elif opcode == 2:
            f = lambda a, b: a * b
        else:
            raise Exception('Unknown opcode')
        d1, d2, d3 = memory[i+1], memory[i+2], memory[i+3]
        result = f(memory[d1], memory[d2])
        memory[d3] = result
        i += 4
    i = 0
    out = []
    for k, v in sorted(memory.items()):
        if k < i:
            raise Exception('invalid memory key')
        elif k == i:
            i += 1
        else:
            raise Exception('Handle non contiguous keys, bitch')
        out.append(v)
    return ','.join(map(str, out))


def simulate_program(l: str, i: int, j: int) -> int:
    data = l.split(',')
    data[1] = str(i)
    data[2] = str(j)
    output = run_program(','.join(data))
    other_result = int(output.split(',')[0])
    result = int(output[:output.index(',')])
    assert result == other_result
    return result


def main():
    xs = []
    ys = []
    zs = []
    for l in sys.stdin.readlines():
        l = l.strip()
        if not l:
            continue
        for i in tqdm(range(100)):
            for j in range(100):
                data = simulate_program(l, i, j)
                xs.append(i)
                ys.append(j)
                zs.append(data)
                if data == 19690720:
                    print(i, j)
        # print(run_program(l))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs)
    plt.show()


if __name__ == '__main__':
    main()

