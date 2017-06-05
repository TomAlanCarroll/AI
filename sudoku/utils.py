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


def get_unit(position):
    # Gets all squares in the same unit for a given position
    return [neighbor for neighbor in square_units if position in neighbor][0]


def get_row(position):
    # Gets row from position ('A', 'B', ... 'I')
    return [row for row in row_units if row[0][0] == position][0]


def get_col(position):
    # Gets row from position ('1', '2', ... '9')
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

unit_list_including_diagonals = row_units + column_units + square_units + diagonal_units
