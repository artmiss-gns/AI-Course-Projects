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
    
    def heuristic_1(self, state: State) :
        """Calculates the heuristic score of the current state.
        It counts the number of blocks that are NOT in their correct position.

        Args:
            state (np.array): numpy 3*3 array which represents the state which it's heuristic is calculating
        """
        return 8 - (state.board == self.goal_state.board).sum()

    @staticmethod
    def get_nan_loc(board: np.array) :
        return np.argwhere(np.isnan(board))


    def get_adjacent(
        self,
        state: State,
    ) :
        board = state.board
        nan_loc = np.ravel(self.get_nan_loc(board))
        locs = [
            [nan_loc[0] - 1, nan_loc[1]] if (nan_loc[0] - 1) >= 0 else None, # up
            [nan_loc[0], nan_loc[1] + 1] if (nan_loc[1] + 1) <= board.shape[1]-1 else None, # right
            [nan_loc[0] + 1, nan_loc[1]] if (nan_loc[0] + 1) <= board.shape[0]-1 else None, # down
            [nan_loc[0], nan_loc[1] - 1] if (nan_loc[1] - 1) >= 0 else None, # left
        ]
        return locs

    def switcher(self, state:State, loc) :
        board = state.board
        nan_loc = self.get_nan_loc(board)
        new_board = board.copy()
        new_board[tuple(np.ravel(nan_loc).tolist())], new_board[tuple(loc)] = new_board[tuple(loc)], new_board[tuple(np.ravel(nan_loc).tolist())]
        return new_board

    def get_states(
        self,
        state: State,
    ) :
        states = []
        adjacent_loc = self.get_adjacent(state)
        for loc in adjacent_loc : 
            if loc is not None :
                state = self.switcher(state, loc)
                state = State(
                    board=state
                )
                states.append(state)
                
        return states

    def run(self) :
        """returns a generator that yields states of optimizing puzzle
        """
        previous_state = None
        self.current_state.heuristic_score = self.heuristic_1(self.current_state)

        while self.current_state.heuristic_score > 0 :
            data = {}
            states = self.get_states(self.current_state)
            for state in states :
                heuristic_value = self.heuristic_1(state)
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
    for s in hc.run() :
        print(s)