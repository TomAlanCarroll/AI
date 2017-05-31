from utils import *

assignments = []
elimination_count = 0


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
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
                    print("eliminating in row: " + num + " from " + values[position] + " at " + position)
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
                    print("eliminating in col: " + num + " from " + values[position] + " at " + position)
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
                        print("eliminating in unit: " + num + " from " + values[position] + " at " + position)
                        elimination_count += 1
                        # values[position] = values[position].replace(num, '')
                        values = assign_value(values, position, values[position].replace(num, ''))


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
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

    all_twins = row_twins + col_twins
    eliminate_twins_in_unit_peers(all_twins, values)

    return values


def get_duplicates(dictionary):
    duplicates = []
    values_seen = {}

    for key, val in dictionary.items():
        if val in values_seen.keys():
            duplicates.append(((values_seen[val], val), (key, val)))
        else:
            values_seen[val] = key

    return duplicates


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


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
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_vals = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_vals:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def only_choice(values):
    for unit in unitlist:
        for digit in cols:
            items = [box for box in unit if digit in values[box]]
            if len(items) == 1:
                values = assign_value(values, items[0], digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

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


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    print('Unsolved Sudoku:')
    display(grid_values_with_blanks(diag_sudoku_grid))
    print('\n====================\n')
    print('Solved Sudoku:')
    display(solve(diag_sudoku_grid))

    print("Number of possible values eliminated by naked_twins: ", elimination_count)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
