from src.utils.state_object import State
import numpy as np


def get_nan_loc(board: np.array) :
    return np.argwhere(np.isnan(board))


def get_adjacent(
    state: State,
) :
    board = state.board
    nan_loc = np.ravel(get_nan_loc(board))
    locs = [
        [nan_loc[0] - 1, nan_loc[1]] if (nan_loc[0] - 1) >= 0 else None, # up
        [nan_loc[0], nan_loc[1] + 1] if (nan_loc[1] + 1) <= board.shape[1]-1 else None, # right
        [nan_loc[0] + 1, nan_loc[1]] if (nan_loc[0] + 1) <= board.shape[0]-1 else None, # down
        [nan_loc[0], nan_loc[1] - 1] if (nan_loc[1] - 1) >= 0 else None, # left
    ]
    return locs

def switcher(state:State, loc) :
    board = state.board
    nan_loc = get_nan_loc(board)
    new_board = board.copy()
    new_board[tuple(np.ravel(nan_loc).tolist())], new_board[tuple(loc)] = new_board[tuple(loc)], new_board[tuple(np.ravel(nan_loc).tolist())]
    return new_board

def get_states(
    state: State,
) :
    states = []
    adjacent_loc = get_adjacent(state)
    for loc in adjacent_loc : 
        if loc is not None :
            state = switcher(state, loc)
            state = State(
                board=state
            )
            states.append(state)
            
    return states
