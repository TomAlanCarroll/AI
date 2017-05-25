rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

# Complete 9x9 grid
# ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
#  'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
#  'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
#  ... ]
boxes = cross(rows, cols)

# Row array
# Example: row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
row_units = [cross(r, cols) for r in rows]

# Column Array
# Example: column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
column_units = [cross(rows, c) for c in cols]

# 9 section Square Array
# Example: square_units[0] = ['A1', 'A2', 'A3',
#                             'B1', 'B2', 'B3',
#                             'C1', 'C2', 'C3']
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    assert len(grid) == 81, 'grid for grid_values must be 81 characters'
    grid_dict = dict(zip(boxes, grid))
    for key,val in grid_dict.items():
        if val == '.':
            grid_dict[key] = '123456789'

    return grid_dict

# Tests:
#display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))
#display(grid_values('483921657967345821251876493548132976729564138136798245372689514814253769695417382'))

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_vals = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_vals:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')

    return values

# Tests:
#display(eliminate(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in cols:
            items = [box for box in unit if digit in values[box]]
            if len(items) == 1:
                values[items[0]] = digit
    return values

# Tests:
#display(only_choice(eliminate(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))))

def reduce_puzzle(values):
    stop = False
    stalled = False
    while not stop:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = len([box for box in values.keys() if len(values[box]) > 1]) > 0

        # If no new values were added, stop the loop.
        stop = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    if stalled:
        print("Sudoku puzzle could not be solved")
    else:
        print("Sudoku puzzle solved")

    return values

# Tests:
#display(reduce_puzzle(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))
# Not solvable:
#display(reduce_puzzle(grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')))

