from utils import *

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
# display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))
# display(grid_values('483921657967345821251876493548132976729564138136798245372689514814253769695417382'))