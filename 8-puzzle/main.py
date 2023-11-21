import numpy as np
from dataclasses import dataclass

@dataclass
class State :
    board: np.array
    heuristic_score: int = None
    
    def __str__(self) :
        return f"{self.board}"
    
    def __repr__(self) :
        return f"State({self.board, self.heuristic_score})"
    
    def __hash__(self):
        # Create a hash based on the Numpy array. This fixes the unhashable problem of the class
        return hash(tuple(self.board.flatten()))
    
def heuristic_1(state: State) :
    """Calculates the heuristic score of the current state.
    It counts the number of blocks that are NOT in their correct position.

    Args:
        state (np.array): numpy 3*3 array which represents the state which it's heuristic is calculating
    """
    return 8 - (state.board == goal_state.board).sum()

def get_nan_loc(board) :
    return np.argwhere(np.isnan(board))

def get_adjacent(
    board: np.array,
) :
    nan_loc = np.ravel(get_nan_loc(board))
    locs = [
        [nan_loc[0] - 1, nan_loc[1]] if (nan_loc[0] - 1) >= 0 else None, # up
        [nan_loc[0], nan_loc[1] + 1] if (nan_loc[1] + 1) <= board.shape[1]-1 else None, # right
        [nan_loc[0] + 1, nan_loc[1]] if (nan_loc[0] + 1) <= board.shape[0]-1 else None, # down
        [nan_loc[0], nan_loc[1] - 1] if (nan_loc[1] - 1) >= 0 else None, # left
    ]
    return locs

def switcher(board, loc) :
    nan_loc = get_nan_loc(board)
    new_board = board.copy()
    new_board[tuple(np.ravel(nan_loc).tolist())], new_board[tuple(loc)] = new_board[tuple(loc)], new_board[tuple(np.ravel(nan_loc).tolist())]
    return new_board

def get_states(
    state: State,
) :
    board = state.board
    states = []
    adjacent_loc = get_adjacent(board)
    for loc in adjacent_loc : 
        if loc is not None :
            state = switcher(board, loc)
            state = State(
                board=state
            )
            states.append(state)
            
    return states

# getting the puzzle input 
current_state = State(
    board=np.array(
        [
            [4, 1, 3],
            [2, np.nan, 5],
            [6, 7, 8],
        ]
    )
)

goal_state = State(
    board = np.array(
        [
            [1, 2, 3],
            [4, np.nan, 5],
            [6, 7, 8],
        ]
    )
)

previous_state = None
current_state.heuristic_score = heuristic_1(current_state)
print("Inital Puzzle: ")
print(current_state.board, end="\n\n")

while current_state.heuristic_score > 0 :
    data = {}
    states = get_states(current_state)
    for state in states :
        heuristic_value = heuristic_1(state)
        state.heuristic_score = heuristic_value
        data[state] = state.heuristic_score
    data = sorted(data, key=lambda state: state.heuristic_score) # sort the states based on their heuristic value
    
    tmp_state = current_state # ! Deep Copy needed?
    # # selecting one of top 3 results, the first result has a higher chance. This is done to prevent stucking in Local Minimum
    try : 
        current_state = data[np.random.choice([0, 1, 2], p=[0.7, 0.15, 0.15])] 
    except IndexError : # happens in corner blocks
        current_state = data[np.random.choice([0, 1], p=[0.8, 0.2])] 
    # making sure that we dont go back to the last step's state, it prevents us to stuck in a loop
    while previous_state is not None and np.allclose(previous_state.board, current_state.board, equal_nan=True) :
        try : 
            current_state = data[np.random.choice([0, 1, 2], p=[0.7, 0.15, 0.15])] 
        except IndexError : # happens in corner blocks
            current_state = data[np.random.choice([0, 1], p=[0.8, 0.2])]

    previous_state = tmp_state
    print(current_state.board)
    print(current_state.heuristic_score, end="\n\n")