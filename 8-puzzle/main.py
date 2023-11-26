import numpy as np
from dataclasses import dataclass

from utils.utils import get_states
from heuristics import heuristic_1
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
    
class HillClimbing :
    def __init__(self, initial_state: np.array) -> None:
        self.current_state = State(board=initial_state)
        self.goal_state = State(
            board = np.array(
                [
                    [1, 2, 3],
                    [4, np.nan, 5],
                    [6, 7, 8],
                ]
            )
        )
        self.end = False

    def run(self) :
        """returns a generator that yields states of optimizing puzzle
        """
        previous_state = None
        self.current_state.heuristic_score = heuristic_1(self.current_state, goal_state=self.goal_state)

        while self.current_state.heuristic_score > 0 :
            data = {}
            states = get_states(self.current_state)
            for state in states :
                heuristic_value = heuristic_1(state, goal_state=self.goal_state)
                state.heuristic_score = heuristic_value
                data[state] = state.heuristic_score
            data = sorted(data, key=lambda state: state.heuristic_score) # sort the states based on their heuristic value
            
            tmp_state = self.current_state # ! Deep Copy needed?
            # # selecting one of top 3 results, the first result has a higher chance. This is done to prevent stucking in Local Minimum
            try : 
                self.current_state = data[np.random.choice([0, 1, 2], p=[0.7, 0.15, 0.15])] 
            except IndexError : # happens in corner blocks
                self.current_state = data[np.random.choice([0, 1], p=[0.8, 0.2])] 
            # making sure that we dont go back to the last step's state, it prevents us to stuck in a loop
            while previous_state is not None and np.allclose(previous_state.board, self.current_state.board, equal_nan=True) :
                try : 
                    self.current_state = data[np.random.choice([0, 1, 2], p=[0.7, 0.15, 0.15])] 
                except IndexError : # happens in corner blocks
                    self.current_state = data[np.random.choice([0, 1], p=[0.8, 0.2])]

            previous_state = tmp_state
            yield self.current_state.board

        self.end = True
        return




if __name__ == "__main__" :
    # getting the puzzle input 
    initial_state = np.array(
        [
            [4, 1, 3],
            [2, np.nan, 5],
            [6, 7, 8],
        ]
    )
    hc = HillClimbing(initial_state)
    epoch = 0
    while not hc.end :
        if epoch >= 50 : # restarting after 50 iterations
            hc = HillClimbing(initial_state)
            epoch = 0
        for s in hc.run() :
            print(s)