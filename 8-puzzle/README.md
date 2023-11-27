# 8 Puzzle Solver

## Description
This project implements a 8-puzzle solver using a `hill climbing`` optimization algorithm.

The puzzle consists of an N x N grid with tiles numbered 1 through N^2 - 1, plus one empty space. The tiles can slide into the empty space, allowing the puzzle to be solved through sequence of moves.

The solver works by:

1. Accepting an initial puzzle state from the user
2. Applying heuristic optimizations to find better states
3. Repeatedly adjusting the puzzle towards the goal state
4. Displaying each intermediate state back to the user

The project consists of:

- `src` - Core logic 
    - `main.py`: Implements hill climbing algorithm
    - `heuristics.py`: Heuristic functions to evaluate puzzle states 
    - `utils`: Helper functions and classes
- `ui` - User interface 
    - `run.py`: Streamlit app for configuring, running, and visualizing solver

## Usage

To run the puzzle solver:

```bash
streamlit run ui/run.p
```

This will launch the Streamlit web interface to set the puzzle, start solving, and watch the sequence of moves.

Alternatively, the core solver can be tested directly:

```bash
python3 src/main.py
```

This will run the optimization on a default puzzle input without the UI.

## Installation

Requires Python 3.9+

Install requirements:

```bash
pip install -r requirements.txt
```