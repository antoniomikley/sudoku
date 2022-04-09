from sudoku import *

def naked_single(sudoku_to_solve):
    grid = sudoku_to_solve
    for square in grid.squares:
        if len(square.possible_numbers) == 1:
            square.assign_number(square.possible_numbers[0])

def hidden_single(sudoku_to_solve):
    grid = sudoku_to_solve
    for i in range(0,9):
        possible_num_in_col_row_reg = []
        for square in grid.columns[i]:
            if square.number == 0:
                possible_num_in_col_row_reg.extend(square.possible_numbers)
        for n in range(1, 10):
            if possible_num_in_col_row_reg.count(n) == 1:
                for square in grid.columns[i]:
                    square.assign_number(n)
        possible_num_in_col_row_reg = []
        for square in grid.rows[i]:
            if square.number == 0:
                possible_num_in_col_row_reg.extend(square.possible_numbers)
        for n in range(1, 10):
            if possible_num_in_col_row_reg.count(n) == 1:
                for square in grid.rows[i]:
                    square.assign_number(n)
        possible_num_in_col_row_reg = []
        for square in grid.regions[i]:
            if square.number == 0:
                possible_num_in_col_row_reg.extend(square.possible_numbers)
        for n in range(1, 10):
            if possible_num_in_col_row_reg.count(n) == 1:
                for square in grid.regions[i]:
                    square.assign_number(n)

