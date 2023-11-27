from src.utils.state_object import State

def heuristic_1(state: State, goal_state:State) :
    """Calculates the heuristic score of the current state.
    It counts the number of blocks that are NOT in their correct position.

    Args:
        state (np.array): numpy 3*3 array which represents the state which it's heuristic is calculating
    """
    return 8 - (state.board == goal_state.board).sum()

import numpy as np

def heuristic_2(state: State, goal_state: State):
    """Calculates the heuristic score of the current state based on Euclidean distance.

    Args:
        state (np.array): 3x3 numpy array representing the current state.
        goal_state (np.array): 3x3 numpy array representing the goal state.

    Returns:
        int: Heuristic score (estimated cost) based on Euclidean distance.
    """
    heuristic_score = 0
    for i in range(3):
        for j in range(3):
            value = state.board[i, j]
            if not np.isnan(value):  # Skip the empty tile (represented as 0)
                # Find the position of the value in the goal state
                goal_position = np.where(goal_state.board == value)
                # Calculate the Euclidean distance for each value from its goal position
                heuristic_score += np.linalg.norm([i - goal_position[0][0], j - goal_position[1][0]])
    return int(heuristic_score)
