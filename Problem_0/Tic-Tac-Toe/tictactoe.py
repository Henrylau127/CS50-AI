"""
Tic Tac Toe Player
"""

import copy
import math
import random

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

    # Set the cell to the current player
    else:
        boardClone[action[0]][action[1]] = currentPlayer

    return boardClone


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0, len(board) - 1):
        # check rows from top to bottom
        if (board[i][0] == board[i][1] == board[i][2] != EMPTY) and (board[i][0] != EMPTY):
            return board[i][0]

        # check columns from left to right
        if (board[0][i] == board[1][i] == board[2][i] != EMPTY) and (board[0][i] != EMPTY):
            return board[0][i]

    # check diagonals
    # Top left to bottom right
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY) and (board[0][0] != EMPTY):
        return board[0][0]
    # Top right to bottom left
    if (board[0][2] == board[1][1] == board[2][0] != EMPTY) and (board[0][2] != EMPTY):
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    roundResult = winner(board)

    # if there is a winner (I.E: GG), return True
    if roundResult is not None:
        return True

    # check is there is still empty cell unfilled
    for iIndex, i in enumerate(board):
        for jIndex, j in enumerate(i):
            # Some cells are empty, game is still on the way
            if j == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winPlayer = winner(board)

    if winPlayer == X:
        return 1
    elif winPlayer == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    The minimax algorithm, max_value and min_value are based on the pseudocode in the lecture 0.
    """
    # NTS: Player X = As low as possible, Player O = As high as possible
    currentPlayer = player(board)
    optimalAction = []

    # first round, return a random action as any cell is an acceptable solution
    if board == initial_state():
        optimalAction = (random.randint(0, 2), random.randint(0, 2))
        return optimalAction

    # game over
    if terminal(board):
        return None

    # game is not over yet
    else:
        # player X's turn
        if currentPlayer == X:
            possibleActions = actions(board)
            bestValue = -math.inf

            for action in possibleActions:
                # get the value of the action
                value = min_value(result(board, action))
                # check if the value is better than the current best value
                if value > bestValue:
                    bestValue = value
                    optimalAction = action

            return optimalAction

        # player O's turn
        else:
            possibleActions = actions(board)
            bestValue = math.inf

            for action in possibleActions:
                # get the value of the action
                value = max_value(result(board, action))
                # check if the value is better than the current best value
                if value < bestValue:
                    bestValue = value
                    optimalAction = action

            return optimalAction


def max_value(board):
    """
    Returns the maximum possible value of the current board
    """
    value = -math.inf

    # game is over
    if terminal(board):
        return utility(board)

    # game is not over yet, find the best possible move for player X
    else:
        for action in actions(board):
            value = max(value, min_value(result(board, action)))
        return value


def min_value(board):
    """
    Returns the minimum possible value of the current board
    """
    value = math.inf

    # game is over
    if terminal(board):
        return utility(board)

    # game is not over yet, find the best possible move for player O
    else:
        for action in actions(board):
            value = min(value, max_value(result(board, action)))
        return value
