from sudoku import *

def naked_single(sudoku_to_solve):
    grid = sudoku_to_solve
    for square in grid.squares:
        if len(square.possible_numbers) == 1:
            square.assign_number(square.possible_numbers[0])

