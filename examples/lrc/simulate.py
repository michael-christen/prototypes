#!/usr/bin/env python3

import csv
import enum
import copy
import collections
import random
from typing import Dict, List, Tuple, NamedTuple

from tqdm import tqdm


# Probability, Counts, Index / turn
# TODO: Get rid of probability, not tracking
State = Tuple[float, List[int], int]


class State(object):
    probability: float
    coins: List[int]
    index: int

    def __init__(self, *, probability: float, coins: List[int], index: int):
        self.probability = probability
        self.coins = coins
        self.index = index


class Rolls(enum.Enum):
    L = 'L'
    R = 'R'
    C = 'C'
    S = 'S'

    def val(self) -> float:
        if self.value == 'S':
            return 1/2.0
        else:
            return 1/6.0


_LEVELS = [
    Rolls.L,
    Rolls.R,
    Rolls.C,
    Rolls.S,
]
num = 0
_THRESHOLDS = []
for lvl in _LEVELS:
    num += lvl.val()
    _THRESHOLDS.append(num)

def roll() -> Rolls:
    r = random.random()
    for i, thresh in enumerate(_THRESHOLDS):
        if r < thresh:
            return _LEVELS[i]
    raise ValueError('random invalid')


# NOTE: Deterministically searching space would get way too large way too
# quickly
def search(initial_state: State, max_depth: int):
    # BFS or iterative depth first search
    depth = 0

    q = collections.deque()
    q.append(initial_state)

    while depth < max_depth:
        depth += 1
    roll()


def is_last_turn(state: State):
    return len(list(filter(lambda x: x > 0, state.coins))) <= 1


class GameResults(object):
    number_of_turns: int
    max_coins: int
    winning_number_of_coins: int
    no_winner: bool
    winner_index: int

    @classmethod
    def get_fields(cls) -> List[str]:
        return ['number_of_turns', 'max_coins', 'winning_number_of_coins',
                'winner_index']

    def as_row(self) -> Dict[str, int]:
        return {
            'number_of_turns': self.number_of_turns,
            'max_coins': self.max_coins,
            'winning_number_of_coins': self.winning_number_of_coins,
            'winner_index': self.winner_index,
        }

    def __str__(self) -> str:
        win_str = f'{self.winner_index} w/ {self.winning_number_of_coins}'
        return (
            f'{win_str} won. # {self.number_of_turns}, max {self.max_coins}')


def play(initial_state: State, verbose: bool):
    state = initial_state
    count = 0
    prev_was_last = is_last_turn(state)
    results = GameResults()
    results.max_coins = 0
    while True:
        if verbose:
            print(count, ', '.join(str(x) for x in state.coins))
        results.max_coins = max(state.coins[state.index], results.max_coins)
        state = turn(state)
        count += 1
        # Check last turn
        last_turn = is_last_turn(state)
        if last_turn and prev_was_last:
            if verbose:
                print(count, ', '.join(str(x) for x in state.coins))
            players = [(i, c) for i, c in enumerate(state.coins) if c > 0]
            if len(players) == 0:
                results.winning_number_of_coins = 0
                results.no_winner = True
                results.winner_index = -1
            elif len(players) == 1:
                results.winning_number_of_coins = players[0][1]
                results.no_winner = False
                results.winner_index = players[0][0]
            else:
                raise ValueError('Invalid players at "end of game"')
            results.number_of_turns = count
            return results
        prev_was_last = last_turn


def test_roll(num_times):
    counter = collections.Counter()
    for i in range(num_times):
        counter[roll()] += 1
    return counter


def turn(state: State) -> State:
    next_index = (state.index + 1) % len(state.coins)
    num_coins = state.coins[state.index]
    l, r, c, s = 0, 0, 0, 0
    num_rolls = min(3, num_coins)
    for i in range(num_rolls):
        dice = roll()
        if dice == Rolls.L:
            l += 1
        elif dice == Rolls.R:
            r += 1
        elif dice == Rolls.C:
            c += 1
        elif dice == Rolls.S:
            s += 1
        else:
            raise ValueError('invalid roll')
    new_state = copy.deepcopy(state)
    new_state.coins[state.index] -= num_rolls
    new_state.coins[state.index] += s
    new_state.coins[state.index - 1] += l
    new_state.coins[next_index] += r
    new_state.index = next_index
    return new_state


def main():
    # Experiments to do:
    #   - Change number of players
    #   - Change starting pieces
    #   - Change number of rolls

    # Analyses to do:
    #   - Spread
    #   - Mean / Median
    #   - Useful probability distribution graphs with python
    #   - How many trials to avoid getting bias?
    # max_depth = 3
    # num_players = 10
    # initial_coins = 3
    num_simulations = 10000
    situations = []
    for coins in range(1, 8 + 1):
        for players in range(2, 15 + 1):
            situations.append((coins, players))
    for i, (initial_coins, num_players) in enumerate(situations):
        l = [initial_coins] * num_players
        initial_state = State(probability=1.0, coins=l, index=0)
        results = []
        print(f'{i}/{len(situations)}. C: {initial_coins}, P: {num_players}')
        for _ in tqdm(range(num_simulations)):
            result = play(copy.deepcopy(initial_state), verbose=False)
            results.append(result)
        f_name = f'results/result-num_{num_players}-coins_{initial_coins}.csv'
        with open(f_name, 'w') as f:
            writer = csv.DictWriter(f, GameResults.get_fields())
            writer.writeheader()
            for result in results:
                writer.writerow(result.as_row())


if __name__ == '__main__':
    main()

