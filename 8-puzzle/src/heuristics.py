from src.utils.state_object import State

def heuristic_1(state: State, goal_state:State) :
    """Calculates the heuristic score of the current state.
    It counts the number of blocks that are NOT in their correct position.

    Args:
        state (np.array): numpy 3*3 array which represents the state which it's heuristic is calculating
    """
    return 8 - (state.board == goal_state.board).sum()