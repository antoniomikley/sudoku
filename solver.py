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
        return [square for square in col_row_reg if square.possible_numbers == nums]

    # Sudoku solving techniques
    def naked_single(self):
        for square in self.grid.squares:
            if len(square.possible_numbers) == 1:
                square.assign_number(square.possible_numbers[0])

    def hidden_single(self):
        for n in range(1, 10):
            for column in self.grid.columns:
                if self.get_possible_num_in(column).count(n) == 1:
                    for square in column:
                        square.assign_number(n)
            for row in self.grid.rows:
                if self.get_possible_num_in(row).count(n) == 1:
                    for square in row:
                        square.assign_number(n)
            for region in self.grid.regions:
                if self.get_possible_num_in(region).count(n) == 1:
                    for square in region:
                        square.assign_number(n)

    def locked_candidates(self):
        for n in range(1, 10):
            for region in self.grid.regions:
                if self.get_possible_num_in(region).count(n) == 2:
                    possible_locked_candidates = [square for square in region if n in square.possible_numbers]
                    if possible_locked_candidates[0].column == possible_locked_candidates[1].column:
                        for square in [sq for sq in self.grid.columns[possible_locked_candidates[0].column] if sq not in region]:
                            square.eliminated_numbers.append(n)
                    elif possible_locked_candidates[0].row == possible_locked_candidates[1].row:
                        for square in [sq for sq in self.grid.rows[possible_locked_candidates[0].row] if sq not in region]:
                            square.eliminated_numbers.append(n)
            for column in self.grid.columns:
                if self.get_possible_num_in(column).count(n) == 2:
                    possible_locked_candidates = [square for square in column if n in square.possible_numbers]
                    if possible_locked_candidates[0].region == possible_locked_candidates[1].region:
                        for square in [sq for sq in self.grid.regions[possible_locked_candidates[0].region] if sq not in column]:
                            square.eliminated_numbers.append(n)
            for row in self.grid.rows:
                if self.get_possible_num_in(row).count(n) == 2:
                    possible_locked_candidates = [square for square in row if n in square.possible_numbers]
                    if possible_locked_candidates[0].region == possible_locked_candidates[1].region:
                        for square in [sq for sq in self.grid.regions[possible_locked_candidates[0].region] if sq not in row]:
                            square.eliminated_numbers.append(n)

    def get_solutions(self):
        for square in self.grid.squares:
            if square.number == 0:
                for n in range(1, 10):
                    if square.assign_number(n):
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

    def x_wing(self):
        for n in range(1, 10):
            x_wing = []
            position = []
            for row in self.grid.rows:
                if self.get_possible_num_in(row).count(n) == 2:
                    x_wing.append([square for square in row if n in square.possible_numbers])
                    position.append([square.column for square in row if n in square.possible_numbers])
            for column in position:
                if position.count(column) != 2:
                    x_wing.pop(position.index(column))
                    position.pop(position.index(column))
            if len(x_wing) == 2:
                for square in self.grid.columns[x_wing[0][0].column]:
                    if square not in x_wing[0] and square not in x_wing[1]:
                        square.eliminated_numbers.append(n)
                for square in self.grid.columns[x_wing[0][1].column]:
                    if square not in x_wing[0] and square not in x_wing[1]:
                        square.eliminated_numbers.append(n)
            x_wing = []
            position = []
            for column in self.grid.columns:
                if self.get_possible_num_in(column).count(n) == 2:
                    x_wing.append([square for square in column if n in square.possible_numbers])
                    position.append([square.row for square in column if n in square.possible_numbers])
            for row in position:
                if position.count(row) != 2:
                    x_wing.pop(position.index(row))
                    position.pop(position.index(row))
            if len(x_wing) == 2:
                for square in self.grid.rows[x_wing[0][0].row]:
                    if square not in x_wing[0] and square not in x_wing[1]:
                        square.eliminated_numbers.append(n)
                for square in self.grid.rows[x_wing[0][1].row]:
                    if square not in x_wing[0] and square not in x_wing[1]:
                        square.eliminated_numbers.append(n)

    def solve(self):
        solved = False
        counter = 0
        level = 0
        while not solved:
            counter_before = counter
            counter = 0
            for square in self.grid.squares:
                if square.number == 0:
                    counter += 1
            if counter == 0:
                return True
            elif counter_before == counter:
                level += 1
            elif counter_before > counter:
                level = 0

            self.naked_single()
            self.hidden_single()
            self.locked_candidates()
            if level >= 1:
                self.naked_pair()
                self.hidden_pair()
            if level >= 2:
                self.naked_triplet()
                self.hidden_triplet()
                self.x_wing()
                self.naked_quad()
                self.hidden_quad()
            if level > 10:
                return False



            


