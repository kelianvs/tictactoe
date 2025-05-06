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
    x_count = sum(row.count(X) for row in board) 
    o_count = sum(row.count(O) for row in board)
    if x_count == o_count:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # empty cells is the set of all possible actions
    actions = set()
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == EMPTY:
                actions.add((i, j))
    return actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """    
    # returns the board that results from the action
    copyboard = copy.deepcopy(board)
    playermove = player(board)
    copyboard[action[0]][action[1]] = playermove
    return copyboard

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # if diagonals is all X or all O
    # if row is all X or all O
    # if all rows[i] are all X or all O
    for row in board:
        if row.count(X) == len(board):
            return X
        elif row.count(O) == len(board):
            return O

    diag = []
    adiag = []

    for i in range(len(board)):
        diag.append(board[i][i])
        adiag.append(board[i][len(board) - 1 - i])
    
    if diag.count(X) == len(board) or adiag.count(X) == len(board):
        return X
    elif diag.count(O) == len(board) or adiag.count(O) == len(board):
        return O

    for i in range(len(board)):
        col = [row[i] for row in board]
        if col.count(X) == len(board):
            return X
        elif col.count(O) == len(board):
            return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if there is a winner or no empty cells
    if winner(board) == X or winner(board) == O:
        return True
    elif sum(row.count(EMPTY) for row in board) == 0:
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game is over, return None

    is_terminal = terminal(board)
    
    if is_terminal:
        return None
    # return the optimal action for the given player
    # maximize for X and minimize for O
    def max_value(board):
        """
        Returns the minimum/maximum value considering the current board state
        and potential board states that could emerge from the current state through recursion.
        """
        if terminal(board): 
            return utility(board) 
        value = -math.inf  
        for action in actions(board): # recusively iterates over all possible actions
            value = max(value, min_value(result(board, action)))  
        return value
    
    def min_value(board):
        if terminal(board):
            return utility(board)
        value = math.inf
        for action in actions(board):
            value = min(value, max_value(result(board, action)))
        return value
    
    current_player = player(board)
    if current_player == X:
        best_scoreX = -math.inf
        best_actionX = None
        # iterate over all actions to find the best action considering the current board state and potential future states considering opponent's moves
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_scoreX:
                best_scoreX = score
                best_actionX = action
        return best_actionX
    else:
        best_scoreO = math.inf
        best_actionO = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_scoreO:
                best_scoreO = score
                best_actionO = action
        return best_actionO