"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    XStepCount = OStepCount = EmptyCount = 0

    # count the number of X, O and EMPTY on the board
    for i in board:
        for j in i:
            if j == X:                    # Cell is X
                XStepCount += 1
            elif j == O:                  # Cell is O
                OStepCount += 1
            elif j == EMPTY:              # Cell is EMPTY/None
                EmptyCount += 1

    # if there is an empty space, return the player who has the next turn
    if EmptyCount > 0:
        if XStepCount > OStepCount:       # it's O's turn if Player X has more steps than Player O
            return O
        elif XStepCount < OStepCount:     # it's X's turn if Player X has fewer steps than Player O
            return X
        else:                             # Default starting player is X
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()

    for iIndex, i in enumerate(board):  # row
        for jIndex, j in enumerate(i):  # column
            if j == EMPTY:              # Add the index of the empty cell to the set
                possibleActions.add((iIndex, jIndex))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    currentPlayer = player(board)
    boardClone = copy.deepcopy(board)

    # check if the range action is within 0 to 2, raise ValueError if not
    for selectedIndex in action:
        if selectedIndex > 2 or selectedIndex < 0:
            raise ValueError("Invalid action")

    # raise ValueError if the cell is not empty
    if boardClone[action[0]][action[1]] != EMPTY:
        raise Exception("Cell already occupied")

    # make the move
    boardClone[action[0]][action[1]] = currentPlayer

    return boardClone


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
