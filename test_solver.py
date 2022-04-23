import pytest
from sudoku import *
from solver import *

# if there is only one possible number for a particular square,
# then it is the right correct number for that square. 
def test_naked_single():
    Ns = Sudoku()
    SudokuSolver = Solver(Ns)
    for n in range(1, 4):
        Ns.rows[0][n].assign_number(n)
    for n in range(4, 7):
        Ns.columns[0][n].assign_number(n)
    for n in range(7,9):
        Ns.regions[0][n].assign_number(n)
    SudokuSolver.naked_single()
    assert Ns.squares[0].number == 9

# if for a column, row or region, there is only one possibilty in which square
# a particular number could be entered, then it is the right number for that square.
# Test only covers the case, when the hidden single is deduced from the possible numbers
# in a region, so cutting out the parts checking the rows and the columns wont affect the 
# results of the test, but it also should not affect the functionality in a real world scenario.. hopefully..
def test_hidden_single():
    Ns = Sudoku()
    SudokuSolver = Solver(Ns)
    Ns.rows[1][0].assign_number(1)
    Ns.rows[1][2].assign_number(3)
    Ns.rows[0][3].assign_number(2)
    Ns.rows[2][8].assign_number(2)
    SudokuSolver.hidden_single()
    assert Ns.rows[1][1].number == 2

# if a number has only two possible squares in their region in which they can be entered and
# these squares are in the same column or row, then this number cannot appear
# in the squares of that column or row that are not part of the region. 
def test_locked_candidates():
    Ns = Sudoku()
    SudokuSolver = Solver(Ns)
    Ns.rows[0][1].assign_number(1)
    Ns.rows[0][2].assign_number(2)
    Ns.rows[1][6].assign_number(3)
    Ns.rows[2][1].assign_number(5)
    Ns.rows[2][2].assign_number(6)
    SudokuSolver.locked_candidates()
    assert SudokuSolver.get_squares_sharing_possible_nums_in(Ns.columns[0], [3]) == [SudokuSolver.grid.columns[0][0], SudokuSolver.grid.columns[0][2]]
    for i in range(3,9):
        assert Ns.columns[0][i].possible_numbers.count(3) == 0


retcode = pytest.main(["-x", __file__])

# if in a column, row or region there are two squares that have the exact same
# two numbers they could possibly hold, then these numbers are not possible candidates
# for the remaining squares in that column, row, or region.
def test_naked_pair():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    SuSolver.grid.rows[0][0].eliminated_numbers = [3, 4, 5, 6, 7, 8, 9]
    SuSolver.grid.rows[0][1].eliminated_numbers = [3, 4, 5, 6, 7, 8, 9]
    SuSolver.grid.columns[0][3].eliminated_numbers = [3, 4, 5, 6, 7, 8, 9]
    SuSolver.naked_pair()
    for i in range(2, 9):
        assert SuSolver.grid.rows[0][i].possible_numbers.count(1) == 0
        assert SuSolver.grid.rows[0][i].possible_numbers.count(2) == 0
        assert SuSolver.grid.regions[0][i].possible_numbers.count(1) == 0
        assert SuSolver.grid.regions[0][i].possible_numbers.count(2) == 0
    for i in range(1, 9):
        if i != 3:
            assert SuSolver.grid.columns[0][i].possible_numbers.count(1) == 0
            assert SuSolver.grid.columns[0][i].possible_numbers.count(2) == 0
