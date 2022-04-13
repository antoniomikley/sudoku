from sudoku import *

class Solver:
    def __init__(self, sudoku_to_solve):
        self.grid = sudoku_to_solve

    def get_possible_num_in_col(self, column):
        possible_num_in_col = []
        for square in self.grid.columns[column]:
            if square.number == 0:
                possible_num_in_col.extend(square.possible_numbers)
        return possible_num_in_col

    def get_possible_num_in_row(self, row):
        possible_num_in_row = []
        for square in self.grid.rows[row]:
            if square.number == 0:
                possible_num_in_row.extend(square.possible_numbers)
        return possible_num_in_row

    def get_possible_num_in_reg(self, region):
        possible_num_in_reg = []
        for square in self.grid.regions[region]:
            if square.number == 0:
                possible_num_in_reg.extend(square.possible_numbers)
        return possible_num_in_reg

    def get_squares_column_sharing_possible_num(self, column, num):
        squares_sharing_pos_num = [square for square in self.grid.columns[column] if num in square.possible_numbers]
        return squares_sharing_pos_num

    def get_squares_row_sharing_possible_num(self, row, num):
        squares_sharing_pos_num = [square for square in self.grid.rows[row] if num in square.possible_numbers]
        return squares_sharing_pos_num

    def get_squares_region_sharing_possible_num(self, region, num):
        squares_sharing_pos_num = [square for square in self.grid.regions[region] if num in square.possible_numbers]
        return squares_sharing_pos_num

    # Sudoku solving techniques
    def naked_single(self):
        for square in self.grid.squares:
            if len(square.possible_numbers) == 1:
                square.assign_number(square.possible_numbers[0])

    def hidden_single(self):
        for i in range(0,9):
            for n in range(1, 10):
                if self.get_possible_num_in_col(i).count(n) == 1:
                    for square in self.grid.columns[i]:
                        square.assign_number(n)
                if self.get_possible_num_in_row(i).count(n) == 1:
                    for square in self.grid.rows[i]:
                        square.assign_number(n)
                if self.get_possible_num_in_reg(i).count(n) == 1:
                    for square in self.grid.rows[i]:
                        square.assign_number(n)

    def locked_candidates(self):
        for i in range(0,9):
            for n in range(1, 10):
                if self.get_possible_num_in_reg(i).count(n) == 2:
                    squares_with_number_n = self.get_squares_region_sharing_possible_num(i, n)
                    if squares_with_number_n[0].column == squares_with_number_n[1].column:
                        for square in self.grid.columns[squares_with_number_n[0].column]:
                            if square.region != squares_with_number_n[0].region:
                                square.eliminated_numbers.append(n)
                    elif squares_with_number_n[0].row == squares_with_number_n[1].row:
                        for square in self.grid.rows[squares_with_number_n[0].row]:
                            if square.region != squares_with_number_n[0].region:
                                square.eliminated_numbers.append(n)

