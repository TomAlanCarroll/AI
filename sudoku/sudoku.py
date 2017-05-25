from utils import *

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    solution = reduce_puzzle(values)

    if solution is False:
        return False

    # If solved by reduce_puzzle return the solution
    if len([box for box in solution.keys() if len(values[box]) == 1]) == 81:
        return solution
    else:
        # Choose one of the unfilled squares with the fewest possibilities
        n, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
        for value in values[box]:
            sudoku_copy = values.copy()
            sudoku_copy[box] = value

            # recurse the copy
            attempt = search(sudoku_copy)
            if attempt:
                return attempt

# Tests
#display(reduce_puzzle(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))
# Hard sudoku puzzle
#print("Hard sudoku puzzle:")
#display(search(grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')))