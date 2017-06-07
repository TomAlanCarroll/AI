"""
Solution for solving Sudoku puzzles
"""

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    """
    Cross product of elements in A and elements in B.
    """
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


def get_unit(position):
    """
    Gets all squares in the same unit for a given position
    """
    # Gets all squares in the same unit for a given position
    return [neighbor for neighbor in square_units if position in neighbor][0]


def get_row(position):
    """
    Gets row from position ('A', 'B', ... 'I')
    """
    return [row for row in row_units if row[0][0] == position][0]


def get_col(position):
    """
    Gets row from position ('1', '2', ... '9')
    """
    return [col for col in column_units if col[0][1] == position][0]

diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
             ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]


def get_diagonal_1():
    return diagonal_units[0]


def get_diagonal_2():
    return diagonal_units[1]


unit_list = row_units + column_units + square_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# The unit list which includes the two main diagonals for diagonal Sudoku
unit_list_including_diagonals = row_units + column_units + square_units + diagonal_units

assignments = []
elimination_count = 0
iteration_count = 0
reduction_count = 0


def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    """
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def eliminate_twins_in_row_peers(twins, values):
    """
    Eliminate the values of twins as possibilities for their row peers
    Example structure of twins:
    [(('F8', '12'), ('F9', '12')), (('I3', '79'), ('I7', '79'))]
    """
    global elimination_count
    for twin_tuple in twins:
        first_twin = twin_tuple[0][0]
        second_twin = twin_tuple[1][0]
        twin_value = twin_tuple[0][1]  # == twin_tuple[1][1]
        for num in twin_value:
            row_to_eliminate = get_row(first_twin[0])
            for position in row_to_eliminate:
                if position != first_twin and position != second_twin and num in values[position]:
                    #print("Eliminating in row: " + num + " from " + values[position] + " at " + position)
                    elimination_count += 1
                    # values[position] = values[position].replace(num, '')
                    values = assign_value(values, position, values[position].replace(num, ''))


def eliminate_twins_in_column_peers(twins, values):
    """
    Eliminate the values of twins as possibilities for their column peers
    Example structure of twins:
    [(('H7', '79'), ('I7', '79'))]
    """
    global elimination_count
    for twin_tuple in twins:
        first_twin = twin_tuple[0][0]
        second_twin = twin_tuple[1][0]
        twin_value = twin_tuple[0][1]  # == twin_tuple[1][1]
        for num in twin_value:
            col_to_eliminate = get_col(first_twin[1])
            for position in col_to_eliminate:
                if position != first_twin and position != second_twin and num in values[position]:
                    #print("Eliminating in col: " + num + " from " + values[position] + " at " + position)
                    elimination_count += 1
                    # values[position] = values[position].replace(num, '')
                    values = assign_value(values, position, values[position].replace(num, ''))


def eliminate_twins_in_unit_peers(all_twins, values):
    """
    Eliminate the values of twins as possibilities for their column peers
    Example structure of twins:
    [(('H7', '79'), ('I7', '79'))]
    """
    global elimination_count
    for twin_tuple in all_twins:
        first_twin = twin_tuple[0][0]
        second_twin = twin_tuple[1][0]
        twin_value = twin_tuple[0][1]  # == twin_tuple[1][1]
        for num in twin_value:
            unit_to_eliminate = get_unit(first_twin)
            if unit_to_eliminate == get_unit(second_twin):  # Only eliminate if both twins are in the same unit
                for position in unit_to_eliminate:
                    if position != first_twin and position != second_twin and num in values[position]:
                        #print("Eliminating in unit: " + num + " from " + values[position] + " at " + position)
                        elimination_count += 1
                        # values[position] = values[position].replace(num, '')
                        values = assign_value(values, position, values[position].replace(num, ''))


def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # First for rows
    row_twins = []
    col_twins = []

    for row in row_units:
        possible_twins = dict((k, values[k]) for k in row if k in values and len(values[k]) == 2)
        row_twins += get_duplicates(possible_twins)

    eliminate_twins_in_row_peers(row_twins, values)

    for col in column_units:
        possible_twins = dict((k, values[k]) for k in col if k in values and len(values[k]) == 2)
        col_twins += get_duplicates(possible_twins)

    eliminate_twins_in_column_peers(col_twins, values)

    all_twins = row_twins + col_twins
    eliminate_twins_in_unit_peers(all_twins, values)

    return values


def get_duplicates(dictionary):
    """
    Gets a list of tuples for value duplicates within the provided dictionary
    """
    duplicates = []
    values_seen = {}

    for key, val in dictionary.items():
        if val in values_seen.keys():
            duplicates.append(((values_seen[val], val), (key, val)))
        else:
            values_seen[val] = key

    return duplicates


def grid_values_with_blanks(grid):
    """
    Convert grid into a dict of {square: char} with '_' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, 'grid for grid_values must be 81 characters'
    grid_dict = dict(zip(boxes, grid))
    for key, val in grid_dict.items():
        if val == '.':
            grid_dict[key] = '_'

    return grid_dict


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, 'grid for grid_values must be 81 characters'
    grid_dict = dict(zip(boxes, grid))
    for key, val in grid_dict.items():
        if val == '.':
            grid_dict[key] = '123456789'

    return grid_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in values)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values, enforce_diagonals):
    solved_vals = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_vals:
        digit = values[box]

        if enforce_diagonals:
            values = eliminate_in_diagonals(box, digit, values)

        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))

    return values

def eliminate_in_diagonals(solved_box, digit, values):
    if solved_box in get_diagonal_1():
        for diagonal_peer in get_diagonal_1():
            if diagonal_peer != solved_box:
                values = assign_value(values, diagonal_peer, values[diagonal_peer].replace(digit, ''))

    if solved_box in get_diagonal_2():
        for diagonal_peer in get_diagonal_2():
            if diagonal_peer != solved_box:
                values = assign_value(values, diagonal_peer, values[diagonal_peer].replace(digit, ''))

    return values

def only_choice(values, enforce_diagonals):

    for unit in unit_list_including_diagonals if enforce_diagonals else unit_list:
        for digit in cols:
            items = [box for box in unit if digit in values[box]]
            if len(items) == 1:
                values = assign_value(values, items[0], digit)
    return values


def reduce_puzzle(values, enforce_diagonals):
    stalled = False
    global reduction_count
    while not stalled:
        reduction_count += 1

        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values, enforce_diagonals)

        # Use the Only Choice Strategy
        values = only_choice(values, enforce_diagonals)

        # Use the Naked Twin Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def unique_values(grid):
    seen = set()
    for x in grid:
        if x in seen:
            return False
        seen.add(x)
    return True


def diagonals_are_unique(solution):
    diagonal1 = get_diagonal_1()
    diagonal2 = get_diagonal_2()

    seen = set()

    for box in diagonal1:
        if solution[box] in seen:
            return False  # Diagonal 1 boxes are not unique 1..9
        else:
            seen.add(solution[box])

    seen = set()

    for box in diagonal2:
        if solution[box] in seen:
            return False  # Diagonal 2 boxes are not unique 1..9
        else:
            seen.add(solution[box])

    return True


def search(values, enforce_diagonals):
    global iteration_count
    iteration_count += 1

    # First, reduce the puzzle using the previous function
    solution = reduce_puzzle(values, enforce_diagonals)

    if solution is False:
        return False

    all_boxes_contain_one = len([box for box in solution.keys() if len(values[box]) == 1]) == 81

    # If solved by reduce_puzzle return the solution
    if all_boxes_contain_one:
        return solution
    # elif enforce_diagonals and all_boxes_contain_one and diagonals_are_unique(values):
    #     return solution
    else:
        # Choose one of the unfilled squares with the fewest possibilities
        n, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
        for value in values[box]:
            sudoku_copy = values.copy()
            sudoku_copy[box] = value

            # recurse the copy
            attempt = search(sudoku_copy, enforce_diagonals)
            if attempt:
                return attempt


def solve_sudoku(grid, enforce_diagonals):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
        enforce_diagonals(bool): Enforce that the two main diagonals each contain 1..9 only once
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    global iteration_count, reduction_count
    iteration_count = 0
    reduction_count = 0
    solved = search(grid_values(grid), enforce_diagonals)
    print('Solved in', iteration_count, 'search iterations' if iteration_count > 1 else 'search iteration', 'with',
          reduction_count, 'reduction strategy iterations' if reduction_count > 1 else 'reduction strategy iteration')
    display(solved)
    return solved

def solve(grid):
    """
    Convenience method for tests
    """
    return solve_sudoku(grid, True)

if __name__ == '__main__':
    difficult_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    print('Unsolved Difficult Sudoku:')
    display(grid_values_with_blanks(difficult_sudoku_grid))
    print('\n====================\n')
    print('Solved Difficult Sudoku:')
    solve_sudoku(difficult_sudoku_grid, False)

    print('\n----------------------------------------\n')

    diagonal_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    print('Unsolved Diagonal Sudoku:')
    display(grid_values_with_blanks(diagonal_sudoku_grid))
    print('\n====================\n')
    print('Solved Diagonal Sudoku:')
    diagonals = True
    solve_sudoku(diagonal_sudoku_grid, diagonals)

    print("Number of possible values eliminated by naked_twins: ", elimination_count)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
