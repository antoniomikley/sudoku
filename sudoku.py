class Sudoku:
    def __init__(self):
        self.squares = []
        self.columns = []
        self.rows = []
        self.regions = []
        self.create_9_by_9_sudoku()

    def create_9_by_9_sudoku(self):
        for i in range(0, 10):
            self.columns.append([])
            self.rows.append([])
            self.regions.append([])
        for n in range(0, 81):
            col = n % 9
            row = n // 9
            reg = col // 3 + row // 3 * 3
            self.squares.append(Square(col, row, reg, self))
            self.columns[col].append(self.squares[n])
            self.rows[row].append(self.squares[n])
            self.regions[reg].append(self.squares[n])
    
    def input_numbers(self, sudoku: list):
        for i in range(0, len(sudoku) -1):
            self.squares[i].assign_number(sudoku[i])


class Square:
    def __init__(self, column, row, region, grid):
        self.column = column
        self.row = row
        self.region = region
        self.number = 0
        self.grid = grid
        self.eliminated_numbers = []

    @property
    def possible_numbers(self):
        if self.number == 0:
            possible_numbers = [n for n in range(1, 10) if n not in self.invalid_numbers]
            return possible_numbers
        else:
            return []

    @property
    def invalid_numbers(self):
        invalid_numbers = self.get_numbers_in_same_column() + self.get_numbers_in_same_row() + self.get_numbers_in_same_region() + self.eliminated_numbers
        return invalid_numbers

    def assign_number(self, num):
        if self.number == 0 and num in self.possible_numbers:
            self.number = num

    def get_numbers_in_same_column(self):
        numbers_same_column = []
        for n in range(0, 9):
            numbers_same_column.append(self.grid.columns[self.column][n].number)
        return numbers_same_column

    def get_numbers_in_same_row(self):
        numbers_same_row = []
        for n in range(0, 9):
            numbers_same_row.append(self.grid.rows[self.row][n].number)
        return numbers_same_row

    def get_numbers_in_same_region(self):
        numbers_same_region = []
        for n in range(0, 9):
            numbers_same_region.append(self.grid.regions[self.region][n].number)
        return numbers_same_region

