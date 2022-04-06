class Sudoku:
    def __init__(self):
        self.squares = []
        self.columns = {}
        self.rows = {}
        self.regions = {}
        self.create_9_by_9_grid_of_squares()

    def create_9_by_9_grid_of_squares(self):
        for n in range(0, 81):
            column = n % 9
            row = n // 9
            region = column // 3 + row // 3 * 3
            self.squares.append(Square(column, row, region))
            if n == 0:
                for i in range(0, 9):
                    self.columns[i] = []
                    self.rows[i] = []
                    self. regions[i] = []
            self.columns[column].append(self.squares[n])
            self.rows[row].append(self.squares[n])
            self.regions[region].append(self.squares[n])

class Square():
    def __init__(self, column = None, row = None, region = None):
        self.column = column
        self.row = row
        self.region = region
        self.number = None
        self.possible_numbers = set([1, 2 ,3 ,4 ,5 ,6 ,7 ,8 ,9])

    def is_empty(self):
        if self.number == None:
            return True
        else:
            return False

    def assign_number(self, num):
        if self.is_empty() and num in self.possible_numbers:
           self.number = num

