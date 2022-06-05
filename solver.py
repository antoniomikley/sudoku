from sudoku import *


class Solver:
    def __init__(self, sudoku_to_solve):
        self.grid = sudoku_to_solve
        self.solutions = []

    def get_possible_num_in(self, col_row_reg: list):
        pos_nums = []
        for square in col_row_reg:
            pos_nums.extend(square.possible_numbers)
        return pos_nums

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
        for region in self.grid.regions:
            for n in range (1, 10):
                if self.get_possible_num_in(region).count(n) == 2:
                    possible_locked_candidates = [square for square in region if n in square.possible_numbers]
                    if possible_locked_candidates[0].column == possible_locked_candidates[1].column:
                        for square in [sq for sq in self.grid.columns[possible_locked_candidates[0].column] if sq not in region]:
                            square.eliminated_numbers.append(n)
                    if possible_locked_candidates[0].row == possible_locked_candidates[1].row:
                        for square in [sq for sq in self.grid.rows[possible_locked_candidates[0].row] if sq not in region]:
                            square.eliminated_numbers.append(n)

    def get_solutions(self):
        for square in self.grid.squares:
            if square.number == 0:
                for n in range(1, 10):
                    if n in square.possible_numbers:
                        square.number = n
                        self.get_solutions()
                        square.number = 0
                return
        self.solutions.append([square.number for square in self.grid.squares])

    def naked_base(self, col_row_reg, n):
        possible_naked_triplets = [square for square in col_row_reg if len(square.possible_numbers) <= n and square.possible_numbers != []]
        if len(possible_naked_triplets) < n:
            return False
        naked_triplets = [possible_naked_triplets[0]]
        naked_candidates = set(naked_triplets[0].possible_numbers)
        possible_naked_triplets.pop(0)
        for square in possible_naked_triplets:
            if len(naked_candidates.union(set(square.possible_numbers))) <= n:
                naked_triplets.append(square)
                naked_candidates.update(set(square.possible_numbers))
        if len(naked_triplets) == n:
            for square in col_row_reg:
                if square not in naked_triplets:
                    square.eliminated_numbers.extend(list(naked_candidates))
            return True
        self.naked_base(possible_naked_triplets, n)
   
    def naked_pair(self):
        self.naked_triplet(2)

    def naked_triplet(self, n = 3):
        for row in self.grid.rows:
            self.naked_base(row, n)
        for column in self.grid.columns:
            self.naked_base(column, n)
        for region in self.grid.regions:
            self.naked_base(region, n)

    def naked_quad(self):
        self.naked_triplet(4)

    def hidden_base(self, col_row_reg, i):
        possible_hidden_pairs = []
        for n in range(1, 10):
            if self.get_possible_num_in(col_row_reg).count(n) <= i:
                possible_hidden_pairs.append([square for square in col_row_reg if n in square.possible_numbers])
        for pair in possible_hidden_pairs:
            if possible_hidden_pairs.count(pair) <= i != 0 and pair != []:
                eliminated_candidates = set(self.get_possible_num_in([square for square in col_row_reg if square not in pair]))
                for square in pair:
                    square.eliminated_numbers.extend(list(eliminated_candidates))
                return True

    def hidden_pair(self, i = 2):
        for column in self.grid.columns:
            self.hidden_base(column, i)
        for row in self.grid.rows:
            self.hidden_base(row, i)
        for region in self.grid.regions:
            self.hidden_base(region, i)

    def hidden_triplet(self):
        self.hidden_pair(3)

    def hidden_quad(self):
        self.hidden_pair(4)
