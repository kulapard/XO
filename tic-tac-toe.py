#!/bin/python
import random
from copy import deepcopy

X = chr(88)
O = chr(79)
EMPTY = chr(95)
SIZE = 3


def is_empty(state):
    count_x = 0
    count_o = 0
    for row in state:
        count_x += row.count(X)
        count_o += row.count(O)

    if count_x == count_o == 0:
        return True

    return False


def actions(state):
    for r, row in enumerate(state):
        for c, col in enumerate(row):
            if col == EMPTY:
                yield (r, c)


def update_state(state, action, player):
    new_state = deepcopy(state)
    r, c = action
    new_state[r][c] = player
    return new_state


def is_game_over(state):
    for i in xrange(SIZE):
        # Vertical
        if state[0][i] == state[1][i] == state[2][i] != EMPTY:
            return True

        # Horizontal
        if state[i][0] == state[i][1] == state[i][2] != EMPTY:
            return True

    # Diagonal
    if state[0][0] == state[1][1] == state[2][2] != EMPTY:
        return True

    if state[2][0] == state[1][1] == state[0][2] != EMPTY:
        return True

    # Check if it is tie
    for row in state:
        if EMPTY in row:
            return False

    return True


def get_result(state, player):
    """Returns result for current player

    1 - win
    0 - tie
    -1 - lose

    :type state: list[list]
    :type player: str
    :rtype: int
    """
    result = 0
    for i in xrange(SIZE):
        if state[0][i] == state[1][i] == state[2][i] != EMPTY:
            result = 1 if state[0][i] == player else -1

        if state[i][0] == state[i][1] == state[i][2] != EMPTY:
            result = 1 if state[i][0] == player else -1

    if state[0][0] == state[1][1] == state[2][2] != EMPTY:
        result = 1 if state[0][0] == player else -1

    if state[2][0] == state[1][1] == state[0][2] != EMPTY:
        result = 1 if state[2][0] == player else -1

    return result


def min_value(state, player):
    if is_game_over(state):
        return get_result(state, player)

    next_player = X if player == O else O
    value = 1
    for a in actions(state):
        next_state = update_state(state, a, next_player)
        value = min(value, max_value(next_state, player))

    return value


def max_value(state, player):
    if is_game_over(state):
        return get_result(state, player)

    value = -1
    for a in actions(state):
        next_state = update_state(state, a, player)
        value = max(value, min_value(next_state, player))

    return value


def minmax(state, player):
    """Returns next optimal action

    :type state: list[list]
    :type player: str
    :rtype: tuple(int, int) | None
    """
    value, action = None, None
    for a in actions(state):
        next_state = update_state(state, a, player)
        v = min_value(next_state, player)

        if value is None or v > value:
            value, action = v, a

    return action


# Complete the function below to print 2 integers separated by a single space which will be your next move
def nextMove(player, board):
    state = map(list, board)
    if is_empty(state):
        action = random.choice(list(actions(state)))
    else:
        action = minmax(state, player)

    if action:
        print '%s %s' % action


# If player is X, I'm the first player.
# If player is O, I'm the second player.
player = raw_input()

# Read the board now. The board is a 3x3 array filled with X, O or _.
board = []
for i in xrange(0, 3):
    board.append(raw_input())

nextMove(player, board)
