#!/usr/bin/env python3
import csv
import collections

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d


def main():
    situations = []
    # for coins in range(1, 8 + 1):
    #     for players in range(2, 15 + 1):
    #         situations.append((coins, players))
    for i in range(3, 16):
        situations.append((3, i))
    data = {}
    for initial_coins, num_players in situations:
        f_name = f'results/result-num_{num_players}-coins_{initial_coins}.csv'
        try:
            with open(f_name, 'r') as f:
                print(initial_coins, num_players)
                reader = csv.DictReader(f)
                rows = []
                for row in reader:
                    rows.append(row)
                data[(initial_coins, num_players)] = rows
        except FileNotFoundError:
            print(f'{f_name} not found')
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(3, 16):
        c = collections.Counter()
        # number_of_turns,max_coins,winning_number_of_coins,winner_index
        for num_turns in [int(r['number_of_turns']) for r in data[(3, i)]]:
            c[num_turns] += 1
        max_num = max(c.keys()) + 1
        min_num = min(c.keys())
        x = range(min_num, max_num)
        y = [c[i] for i in range(min_num, max_num)]
        z = [i] * len(y)
        # plt.plot(x, y)
        ax.plot(x, y, z, zdir='y')
    plt.yscale('linear')
    plt.show()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_wireframe(three_x, three_y, three_z, rstride=10, cstride=10)


if __name__ == '__main__':
    main()

