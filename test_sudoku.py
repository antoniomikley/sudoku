import pytest
from sudoku import *

def test_new_square_is_empty():
    NewSquare = Square()
    assert NewSquare.is_empty()

def test_square_holding_a_number_is_not_empty():
    NewSquare = Square()
    NewSquare.assign_number(1)
    assert NewSquare.is_empty() == False

def test_square_holds_only_integers_between_1_and_9():
    NewSquare = Square()
    NewSquare.assign_number(10)
    assert NewSquare.is_empty()
    NewSquare.assign_number(8)
    assert NewSquare.is_empty() == False and NewSquare.number == 8

def test_new_sudoku_has_81_squares():
    NewSudoku = Sudoku()
    assert len(NewSudoku.squares) == 81
    assert all(isinstance(square, Square) for square in NewSudoku.squares) == True

def test_squares_left_or_right_of_each_other_are_in_the_same_row():
    NewSudoku = Sudoku()
    assert NewSudoku.squares[0].row == NewSudoku.squares[8].row == 0
    assert NewSudoku.squares[9] in NewSudoku.rows[1]
    assert NewSudoku.squares[8] in NewSudoku.rows[0]
    assert NewSudoku.squares[80] in NewSudoku.rows[8]

def test_squares_above_or_beneath_each_other_are_in_the_same_column():
    NewSudoku = Sudoku()
    assert NewSudoku.squares[0].column == NewSudoku.squares[72].column == 0
    assert NewSudoku.squares[40] in NewSudoku.columns[4]
    assert NewSudoku.squares[80] in NewSudoku.columns[8]
    assert NewSudoku.squares[34] in NewSudoku.columns[7]

def test_squares_in_3_by_3_area_on_grid_are_in_the_same_region():
    NewSudoku = Sudoku()
    assert NewSudoku.squares[0].region == NewSudoku.squares[20].region == 0
    assert NewSudoku.squares[13] in NewSudoku.regions[1]
    assert NewSudoku.squares[61] in NewSudoku.regions[8]
    assert NewSudoku.squares[56] in NewSudoku.regions[6]

def test_numbers_are_invalid_for_square_if_already_present_in_same_column():
    NewSudoku = Sudoku()
    NewSudoku.squares[4].assign_number(2)
    NewSudoku.squares[40].assign_number(4)
    NewSudoku.squares[31].assign_number(2)
    NewSudoku.squares[31].assign_number(4)
    assert NewSudoku.squares[31].is_empty()



retcode = pytest.main(["-x", __file__])
