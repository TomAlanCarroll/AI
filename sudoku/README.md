# Sudoku Puzzle Solver
This solves Sudoku puzzles using 3 process-of-elimination strategies and depth-first search.

There are two types of Sudoku puzzles supported:
1. *Regular Sudoku* - Where each row, column, and 3x3 unit must contain 1 to 9 exactly once.
1. *Diagonal Sudoku* - Same rules for *Regular Sudoku* with the additional criteria that each of the 2 main diagonals in the puzzle must contain 1 to 9 exactly once.

## How do we apply constraint propagation to solve the naked twins problem?
Constraint propagation has been used to implement the naked twins strategy by enforcing the constraint that no squares outside the two naked twins squares can contain the twin values within the respective row, column, or 3x3 unit. This process-of-elimination strategy was implemented as follows:

1. For each row in the puzzle, find all twins that can be eliminated and remove them from their relative rows.
1. For each column in the puzzle, find all twins that can be eliminated and remove them from their relative columns.
1. For each 3x3 unit in the puzzle, find all twins that can be eliminated and remove them from their relative unit.

It is important to note that twin elimination may not necessarily extend outside of twins' rows, columns, or units.

## How do we apply constraint propagation to solve the diagonal sudoku problem?
Constraint propagation has been used to solve the diagonal sudoku by adding the diagonals to the set of constraints. This was done by adding the main 2 diagonals to the set of 3x3 units for the sudoku puzzle. In this way the diagonal constraint was enforced for depth-first search.

## How to Run
1. Follow the setup instructions in the AI [README.md](../README.md)
1. Run the following commands:

```
cd sudoku
python3 solution.py
python3 solution_test.py
```

## 1. Difficult Sudoku Puzzle
A difficult Sudoku puzzle is the first to be solved.

```
Unsolved Difficult Sudoku:
4 _ _ |_ _ _ |8 _ 5
_ 3 _ |_ _ _ |_ _ _
_ _ _ |7 _ _ |_ _ _
------+------+------
_ 2 _ |_ _ _ |_ 6 _
_ _ _ |_ 8 _ |4 _ _
_ _ _ |_ 1 _ |_ _ _
------+------+------
_ _ _ |6 _ 3 |_ 7 _
5 _ _ |2 _ _ |_ _ _
1 _ 4 |_ _ _ |_ _ _
```

This puzzle was solved with 5 depth first search iterations and a total of 18 reduction strategy iterations:

```
Solved Difficult Sudoku:
Solved in 5 search iterations with 18 reduction strategy iterations
4 1 7 |3 6 9 |8 2 5
6 3 2 |1 5 8 |9 4 7
9 5 8 |7 2 4 |3 1 6
------+------+------
8 2 5 |4 3 7 |1 6 9
7 9 1 |5 8 6 |4 3 2
3 4 6 |9 1 2 |7 5 8
------+------+------
2 8 9 |6 4 3 |5 7 1
5 7 3 |2 9 1 |6 8 4
1 6 4 |8 7 5 |2 9 3
```

If you installed pygame the puzzle solution is shown:
![images/difficult-sudoku.png](Difficult Sudoku Solution)

## 2. Diagonal Sudoku Puzzle
A Sudoku puzzle with the diagonal constraints is the second to be solved.

```
Unsolved Diagonal Sudoku:
2 _ _ |_ _ _ |_ _ _
_ _ _ |_ _ 6 |2 _ _
_ _ 1 |_ _ _ |_ 7 _
------+------+------
_ _ 6 |_ _ 8 |_ _ _
3 _ _ |_ 9 _ |_ _ 7
_ _ _ |6 _ _ |4 _ _
------+------+------
_ 4 _ |_ _ _ |8 _ _
_ _ 5 |2 _ _ |_ _ _
_ _ _ |_ _ _ |_ _ 3
```

```
Solved Diagonal Sudoku:
Solved in 1 search iteration with 13 reduction strategy iterations
2 6 7 |9 4 5 |3 8 1
8 5 3 |7 1 6 |2 4 9
4 9 1 |8 2 3 |5 7 6
------+------+------
5 7 6 |4 3 8 |1 9 2
3 8 4 |1 9 2 |6 5 7
1 2 9 |6 5 7 |4 3 8
------+------+------
6 4 2 |3 7 9 |8 1 5
9 3 5 |2 8 1 |7 6 4
7 1 8 |5 6 4 |9 2 3
```

If you installed pygame the puzzle solution is shown:
![/images/diagonal-sudoku.png](Diagonal Sudoku Solution)