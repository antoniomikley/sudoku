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
    for i in range(3,9):
        assert Ns.columns[0][i].possible_numbers.count(3) == 0

    Ns2 = Sudoku()
    SudokuSolver = Solver(Ns2)
    Ns2.rows[1][0].assign_number(1)
    Ns2.rows[2][0].assign_number(2)
    Ns2.rows[6][1].assign_number(3)
    Ns2.rows[1][2].assign_number(5)
    Ns2.rows[2][2].assign_number(6)
    SudokuSolver.locked_candidates()
    for i in range(3,9):
        assert Ns2.rows[0][i].possible_numbers.count(3) == 0

    Ns3 = Sudoku()
    SuSolver = Solver(Ns3)
    Ns3.rows[0][0].eliminated_numbers = [1, 2, 3, 4, 5, 8, 9]
    Ns3.rows[0][1].eliminated_numbers = [2, 3, 4, 5, 8, 9]
    Ns3.rows[0][2].number = 3
    Ns3.rows[0][3].eliminated_numbers = [2, 3, 4, 5, 7, 8]
    Ns3.rows[0][4].eliminated_numbers = [2, 3, 4, 5, 6, 7]
    Ns3.rows[0][5].eliminated_numbers = [1, 3, 4, 5, 7, 8, 9]
    Ns3.rows[0][6].number = 4 
    Ns3.rows[0][7].eliminated_numbers = [1, 3, 4, 5, 6, 7, 9]
    Ns3.rows[0][8].number = 5
    Ns3.regions[0][3].eliminated_numbers = [1, 2, 3, 4, 5, 6, 9]
    Ns3.regions[0][5].eliminated_numbers = [2, 3, 4, 6, 7, 8, 9]
    Ns3.regions[0][7].eliminated_numbers = [2, 3, 4, 5, 8, 9]
    Ns3.regions[0][4].number = 2
    Ns3.regions[0][6].number = 9
    Ns3.regions[0][8].number = 4
    SuSolver.locked_candidates()
    assert Ns3.regions[0][3].possible_numbers.count(7) == 0
    assert Ns3.regions[0][7].possible_numbers.count(7) == 0



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

'''
def test_get_solutions():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    sudoku_numbers = [
        5, 3, 0, 0, 7, 0, 0, 0, 0,
        6, 0, 0, 1, 9, 5, 0, 0, 0,
        0, 9, 8, 0, 0, 0, 0, 6, 0,
        8, 0, 0, 0, 6, 0, 0, 0, 3,
        4, 0, 0, 8, 0, 3, 0, 0, 1,
        7, 0, 0, 0, 2, 0, 0, 0, 6,
        0, 6, 0, 0, 0, 0, 2, 8, 0,
        0, 0, 0, 4, 1, 9, 0 ,0, 5,
        0, 0, 0, 0, 8, 0, 0, 7, 9
        ]
    Ns.input_numbers(sudoku_numbers)
    SuSolver.get_solutions()
    assert SuSolver.solutions == [[
            5, 3, 4, 6, 7, 8, 9, 1, 2,
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7 ,4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9
            ]]
def test_get_all_solutions_if_there_are_multiple():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    sudoku_numbers = [
        5, 3, 0, 0, 7, 0, 0, 0, 0,
        6, 0, 0, 1, 9, 5, 0, 0, 0,
        0, 9, 8, 0, 0, 0, 0, 6, 0,
        8, 0, 0, 0, 6, 0, 0, 0, 3,
        4, 0, 0, 8, 0, 3, 0, 0, 1,
        7, 0, 0, 0, 2, 0, 0, 0, 6,
        0, 6, 0, 0, 0, 0, 2, 0, 0,
        0, 0, 0, 4, 1, 9, 0 ,0, 5,
        0, 0, 0, 0, 8, 0, 0, 7, 9
        ]
    Ns.input_numbers(sudoku_numbers)
    SuSolver.get_solutions()
    assert len(SuSolver.solutions) > 1

'''
# if in a column, row or region there are exactly three squares which possible numbers
# form a set with a total of three unique elements, then these numbers are not possible candidates
# for the other squares in the same column, row or region.
# it is basically the same as a naked pair, but with one more possible candidate involved.
def test_naked_triplet():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    Ns.rows[0][2].eliminated_numbers = [1, 3, 4, 7, 8, 9]
    Ns.rows[0][1].number = 2
    Ns.rows[0][0].eliminated_numbers = [3, 5, 6, 7]
    Ns.rows[0][3].eliminated_numbers = [1, 3, 5, 6, 8, 9]
    Ns.rows[0][4].eliminated_numbers = [1, 3, 4, 5, 7, 9]
    Ns.rows[0][5].eliminated_numbers = [3, 4, 5, 8, 9]
    Ns.rows[0][6].eliminated_numbers = [1, 5, 6, 8]
    Ns.rows[0][7].eliminated_numbers = [1, 6, 8]
    Ns.rows[0][8].eliminated_numbers = [1, 3, 4, 6, 7, 9]
    SuSolver.naked_triplet()
    assert Ns.rows[0][0].possible_numbers == [1, 4, 9]
    assert Ns.rows[0][5].possible_numbers == [1, 7]
    assert Ns.rows[0][7].possible_numbers == [3, 4, 7, 9]

# same as naked triplets but with four squares which possible numbers form a set with four elements
def test_naked_quad():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    Ns.regions[6][0].eliminated_numbers = [2, 3, 4, 5, 6, 7, 8]
    Ns.regions[6][1].number = 5
    Ns.regions[6][2].eliminated_numbers = [2, 4, 5, 7, 9]
    Ns.regions[6][3].eliminated_numbers = [2, 3, 4, 5, 6, 8]
    Ns.regions[6][4].eliminated_numbers = [2, 4, 5, 6, 8]
    Ns.regions[6][5].eliminated_numbers = [2, 4, 5, 6, 7, 8, 9]
    Ns.regions[6][6].eliminated_numbers = [2, 3, 5, 6, 7]
    Ns.regions[6][7].eliminated_numbers = [2, 3, 5, 7, 8]
    Ns.regions[6][8].number = 2
    SuSolver.naked_quad()
    assert Ns.regions[6][2].possible_numbers == [6, 8]
    assert Ns.regions[6][6].possible_numbers == [4, 8]
    assert Ns.regions[6][7].possible_numbers == [4, 6]

# if there is a pair of numbers that are possible candidates for only two 
#squares, then there are no other possible candidates for those two squares
def test_hidden_pair():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    Ns.regions[6][0].number = 3
    Ns.regions[6][1].eliminated_numbers = [1, 2, 3, 6, 7, 9]
    Ns.regions[6][2].number = 1
    Ns.regions[6][3].eliminated_numbers = [1, 2, 3, 6, 8, 9]
    Ns.regions[6][4].number = 2
    Ns.regions[6][5].eliminated_numbers = [1, 2, 3, 6, 7, 8, 9]
    Ns.regions[6][6].eliminated_numbers = [1, 2, 3, 4, 5]
    Ns.regions[6][7].eliminated_numbers = [1, 2, 3, 4, 5, 6, 9]
    Ns.regions[6][8].eliminated_numbers = [1, 2, 3, 4, 5, 7]
    SuSolver.hidden_pair()
    assert Ns.regions[6][6].possible_numbers == [6, 9]
    assert Ns.regions[6][8].possible_numbers == [6, 9]

# same as hidden pair, but with three candidates in three squares
def test_hidden_triplet():    
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    Ns.regions[6][0].eliminated_numbers = [1, 2, 3, 5, 6, 8, 9]
    Ns.regions[6][1].eliminated_numbers = [1, 2, 3, 5, 6, 8]
    Ns.regions[6][2].eliminated_numbers = [1, 2, 5, 6, 7, 8]
    Ns.regions[6][3].eliminated_numbers = [3, 5, 9]
    Ns.regions[6][4].eliminated_numbers = [1, 3, 5]
    Ns.regions[6][5].eliminated_numbers = [2, 3, 5, 6, 7, 8]
    Ns.regions[6][6].eliminated_numbers = [3, 5, 8, 9]
    Ns.regions[6][7].number = 5
    Ns.regions[6][8].eliminated_numbers = [2, 5, 6, 7, 8]
    SuSolver.hidden_triplet()
    assert Ns.regions[6][3].possible_numbers == [2, 6, 8]
    assert Ns.regions[6][4].possible_numbers == [2, 6, 8]
    assert Ns.regions[6][6].possible_numbers == [2, 6]

# same as hidden pair and hidden triplet, but with four numbers. 
# exceedingly rare. I don't even know where it is in the example for this test,
# but there is a hidden quad in this sudoku, so the function should modify the possible numbers
# of the hidden quad. Of course I don't know what those are so this test is super inaccurate,
# however it still has to pass, cause if it does not, then there is definitly smth wrong with this function, 
# but it passing could still mean, that it does not work correctly. 
def test_hidden_quad():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    sudoku_numbers = [
            0, 0, 0, 3, 7, 4, 2, 0, 0,
            0, 0, 0, 0, 8, 2, 0, 4, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 3, 0, 8, 2, 6,
            6, 0, 0, 0, 9, 0, 0, 0, 4,
            8, 0, 5, 0, 4, 6, 9, 7, 0,
            5, 4, 7, 0, 2, 0, 0, 0, 9,
            0, 0, 0, 0, 0, 0, 4, 0, 5,
            0, 1, 0, 4, 5, 0, 7, 0, 2
            ]
    Ns.input_numbers(sudoku_numbers)
    possible_numbers_before = [SuSolver.get_possible_num_in(column) for column in Ns.columns]
    SuSolver.hidden_quad()
    possible_numbers_after = [SuSolver.get_possible_num_in(column) for column in Ns.columns]
    assert possible_numbers_before != possible_numbers_after

# If a number is a possible number for two squares in two different rows (two squares per row)
# and they also share two columns (two of those squares per column) then this number is not a 
# possible number for the remaininig squares in those columns. 
# The same holds true for the case that there are exactly two possibilites for a number in a column.
def test_x_wing():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    sudoku_numbers = [
            7, 4, 3, 2, 9, 5, 8, 1, 6,
            1, 5, 8, 0, 6, 4, 0, 9, 0,
            2, 6, 9, 8, 0, 1, 0, 0, 5,
            4, 8, 6, 0, 1, 9, 5, 0, 0,
            3, 7, 5, 4, 8, 2, 1, 6, 9,
            9, 2, 1, 5, 0, 6, 0, 8, 4,
            5, 3, 4, 6, 2, 8, 9, 7, 1,
            8, 9, 2, 1, 4, 7, 6, 5, 3,
            6, 1, 7, 9, 5, 3, 0, 0, 8
            ]
    Ns.input_numbers(sudoku_numbers)
    possible_numbers_before = [square.possible_numbers for square in Ns.squares if square != Ns.squares[15]]
    SuSolver.x_wing()
    possible_numbers_after = [square.possible_numbers for square in Ns.squares if square != Ns.squares[15]]
    assert Ns.columns[6][1].possible_numbers == [2, 3]
    assert possible_numbers_before == possible_numbers_after

    # same sudoku rotated 90 degrees clockwise
    Ns2 = Sudoku()
    Su2Solver = Solver(Ns2)
    snumbers = [
            6, 8, 5, 9, 3, 4, 2, 1, 7,
            1, 9, 3, 2, 7, 8, 6, 5, 4, 
            7, 2, 4, 1, 5, 6, 9, 8, 3,
            9, 1, 6, 5, 4, 0, 8, 0, 2,
            5, 4, 2, 0, 8, 1, 0, 6, 9,
            3, 7, 8, 6, 2, 9, 1, 4, 5,
            0, 6, 9, 0, 1, 5, 0, 0, 8,
            0, 5, 7, 8, 6, 0, 0, 9, 1,
            8, 3, 1, 4, 9, 0, 5, 0, 6
            ]
    Ns2.input_numbers(snumbers)
    Su2Solver.x_wing()
    assert Ns2.columns[7][6].possible_numbers == [2, 3]
    # another sudoku, since the one before passes also if the first one passes although it shouldn't.  
    Ns3 = Sudoku()
    Su2Solver = Solver(Ns3)
    snumbers = [
            0, 3, 9, 0, 8, 0, 1, 0, 0,
            1, 8, 6, 0, 0, 0, 0, 0, 0,
            0, 2, 4, 0, 1, 0, 0, 8, 3,
            4, 6, 1, 5, 9, 2, 3, 7, 8,
            0, 5, 2, 0, 0, 0, 0, 0, 0,
            0, 9, 7, 0, 6, 0, 5, 0, 0,
            6, 4, 3, 1, 2, 8, 7, 9, 5,
            9, 7, 8, 6, 5, 4, 2, 3, 1,
            2, 1, 5, 3, 7, 9, 8, 0, 0
            ]
    Ns3.input_numbers(snumbers)
    Su2Solver.x_wing()
    assert Ns3.rows[1][3].possible_numbers == [2, 7, 9]
    assert Ns3.rows[1][7].possible_numbers == [2, 5]
    assert Ns3.rows[1][8].possible_numbers == [2, 7, 9]
    assert Ns3.rows[4][3].possible_numbers == [7, 8]
    assert Ns3.rows[4][7].possible_numbers == [1, 6]
    assert Ns3.rows[4][8].possible_numbers == [6, 9]

# crude function to solve a sudoku using the methods above  which are usually applied by humans
# instead of the recursive approach of the get_solutions function, which is a bit boring.
# should work for about 95% of all sudokus in newspapers etc. as long as they are not too difficult and is faster than get_solutions.
# Also means that the sudoku is actually solvable by a human which does not have to be the case for sudokus that are solvable
# through get_solutions
def test_solve():
    Ns = Sudoku()
    SuSolver = Solver(Ns)
    sudoku_numbers = [
        5, 3, 0, 0, 7, 0, 0, 0, 0,
        6, 0, 0, 1, 9, 5, 0, 0, 0,
        0, 9, 8, 0, 0, 0, 0, 6, 0,
        8, 0, 0, 0, 6, 0, 0, 0, 3,
        4, 0, 0, 8, 0, 3, 0, 0, 1,
        7, 0, 0, 0, 2, 0, 0, 0, 6,
        0, 6, 0, 0, 0, 0, 2, 8, 0,
        0, 0, 0, 4, 1, 9, 0 ,0, 5,
        0, 0, 0, 0, 8, 0, 0, 7, 9
        ]
    Ns.input_numbers(sudoku_numbers)
    SuSolver.solve()
    assert [squares.number for squares in Ns.squares] == [
            5, 3, 4, 6, 7, 8, 9, 1, 2,
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7 ,4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9
            ]
