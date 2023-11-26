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