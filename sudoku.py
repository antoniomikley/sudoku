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
        for i in range(0, len(sudoku)):
            if sudoku[i] != 0:
                self.squares[i].number = sudoku[i]
                self.squares[i].locked = True


class Square:
    def __init__(self, column, row, region, grid):
        self.column = column
        self.row = row
        self.region = region
        self.number = 0
        self.grid = grid
        self.eliminated_numbers = []
        self.locked = False

    @property
    def possible_numbers(self):
        if self.locked == False and self.number == 0:
            return [n for n in range(1, 10) if n not in self.invalid_nums + self.eliminated_numbers]
        return []

    def assign_number(self, num):
        if num in self.possible_numbers:
            self.number = num
            return True
        else:
            return False

    @property
    def invalid_nums(self):
        return [square.number for square in self.grid.columns[self.column] + self.grid.rows[self.row] + self.grid.regions[self.region]]

