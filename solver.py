from sudoku import *
from itertools import groupby
from operator import attrgetter

class Solver:
    def __init__(self, sudoku_to_solve):
        self.grid = sudoku_to_solve

    def get_possible_num_in(self, col_row_reg: list):
        pos_nums = []
        for square in col_row_reg:
            if square.number != 0:
                continue
            pos_nums.extend(square.possible_numbers)
        return pos_nums

    def get_squares_sharing_possible_nums_in(self, col_row_reg, nums): 
        squares_sharing_pos_nums = []
        for square in col_row_reg:
            if all([num in square.possible_numbers for num in nums]):
                squares_sharing_pos_nums.append(square)
        return squares_sharing_pos_nums

    def get_square_with_same_possible_nums_in(self, col_row_reg, nums):
        square_with_same_pos_nums = [square for square in col_row_reg if square.possible_numbers == nums]
        return square_with_same_pos_nums

    # Sudoku solving techniques
    def naked_single(self):
        for square in self.grid.squares:
            if len(square.possible_numbers) == 1:
                square.assign_number(square.possible_numbers[0])

    def hidden_single(self):
        for i in range(0,9):
            for n in range(1, 10):
                if self.get_possible_num_in(self.grid.columns[i]).count(n) == 1:
                    for square in self.grid.columns[i]:
                        square.assign_number(n)
                if self.get_possible_num_in(self.grid.rows[i]).count(n) == 1:
                    for square in self.grid.rows[i]:
                        square.assign_number(n)
                if self.get_possible_num_in(self.grid.regions[i]).count(n) == 1:
                    for square in self.grid.rows[i]:
                        square.assign_number(n)

    def locked_candidates(self):
        for i in range(0,9):
            for n in range(1, 10):
                if self.get_possible_num_in(self.grid.regions[i]).count(n) == 2:
                    squares_with_number_n = self.get_squares_sharing_possible_nums_in(self.grid.regions[i], [n])
                    if squares_with_number_n[0].column == squares_with_number_n[1].column:
                        for square in self.grid.columns[squares_with_number_n[0].column]:
                            if square.region != squares_with_number_n[0].region:
                                square.eliminated_numbers.append(n)
                    elif squares_with_number_n[0].row == squares_with_number_n[1].row:
                        for square in self.grid.rows[squares_with_number_n[0].row]:
                            if square.region != squares_with_number_n[0].region:
                                square.eliminated_numbers.append(n)

    def naked_pair(self):
        for i in range(0,9):
            for square in self.grid.columns[i]:
                if len(square.possible_numbers) == 2:
                    possible_naked_pairs = self.get_square_with_same_possible_nums_in(self.grid.columns[i], square.possible_numbers)
                    if len(possible_naked_pairs) == 2 and possible_naked_pairs[0].possible_numbers == possible_naked_pairs[1].possible_numbers:
                        for other_squares in self.grid.columns[i]:
                            if other_squares not in possible_naked_pairs:
                                other_squares.eliminated_numbers += square.possible_numbers
            for square in self.grid.rows[i]:
                if len(square.possible_numbers) == 2:
                    possible_naked_pairs = self.get_square_with_same_possible_nums_in(self.grid.rows[i], square.possible_numbers)
                    if len(possible_naked_pairs) == 2 and possible_naked_pairs[0].possible_numbers == possible_naked_pairs[1].possible_numbers:
                        for other_squares in self.grid.rows[i]:
                            if other_squares not in possible_naked_pairs:
                                other_squares.eliminated_numbers += square.possible_numbers
            for square in self.grid.regions[i]:
                if len(square.possible_numbers) == 2:
                    possible_naked_pairs = self.get_square_with_same_possible_nums_in(self.grid.regions[i], square.possible_numbers)
                    if len(possible_naked_pairs) == 2 and possible_naked_pairs[0].possible_numbers == possible_naked_pairs[1].possible_numbers:
                        for other_squares in self.grid.regions[i]:
                            if other_squares not in possible_naked_pairs:
                                other_squares.eliminated_numbers += square.possible_numbers


