from sudoku import *

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
        return [square for square in col_row_reg if set(nums).issubset(set(square.possible_numbers))]

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

                


    def naked_base(self, n, col_row_reg, pos_set, squares, invalids):
        for square in col_row_reg:
            if square not in squares and len(invalids) < 9:
                if len(set(pos_set)) <= n:
                    pos_set.extend(square.possible_numbers)
                    squares.append(square)
                elif square not in invalids:
                    pos_set.remove(num for num in squares[-1].possible_numbers)
                    squares.pop(-1)
                    invalids.append(square)
                    self.naked_base(n, col_row_reg,pos_set, squares, invalids)
        return squares

    def naked_pair(self):
        for i in range(0, 9):
            self.naked_base(2, self.grid.columns[i], [], [], [])
            self.naked_base(2, self.grid.rows[i], [], [], [])
            self.naked_base(2, self.grid.regions[i], [], [], [])


            
                    
                

        

                    
                    

                    
