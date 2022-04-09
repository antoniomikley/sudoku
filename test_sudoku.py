import pytest
from sudoku import *

def test_new_square_is_empty():
    NewSudoku = Sudoku()
    assert NewSudoku.squares[0].number == 0

def test_square_holding_a_number_is_not_empty():
    NewSudoku = Sudoku() 
    NewSudoku.squares[0].assign_number(5)
    assert NewSudoku.squares[0].number != 0

def test_square_holds_only_integers_between_1_and_9():
    NewSudoku = Sudoku()
    NewSudoku.squares[0].assign_number(10)
    assert NewSudoku.squares[0].number == 0
    NewSudoku.squares[0].assign_number(8)
    assert NewSudoku.squares[0].number != 0 and NewSudoku.squares[0].number == 8
    

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
    for n in range(0, 81):    
        assert NewSudoku.squares[n] in NewSudoku.rows[n // 9]

def test_squares_above_or_beneath_each_other_are_in_the_same_column():
    NewSudoku = Sudoku()
    assert NewSudoku.squares[0].column == NewSudoku.squares[72].column == 0
    assert NewSudoku.squares[40] in NewSudoku.columns[4]
    assert NewSudoku.squares[80] in NewSudoku.columns[8]
    assert NewSudoku.squares[34] in NewSudoku.columns[7]
    for n in range(0, 81):    
        assert NewSudoku.squares[n] in NewSudoku.columns[n % 9]

def test_squares_in_3_by_3_area_on_grid_are_in_the_same_region():
    NewSudoku = Sudoku()
    assert NewSudoku.squares[0].region == NewSudoku.squares[20].region == 0
    assert NewSudoku.squares[13] in NewSudoku.regions[1]
    assert NewSudoku.squares[61] in NewSudoku.regions[8]
    assert NewSudoku.squares[56] in NewSudoku.regions[6]
    assert NewSudoku.squares[12] in NewSudoku.regions[1]
    for n in range(0, 81):    
        assert NewSudoku.squares[n] in NewSudoku.regions[(n % 9) // 3 + (n // 9) // 3 * 3]
    

def test_numbers_are_invalid_for_square_if_already_present_in_same_column():
    NewSudoku = Sudoku() 
    NewSudoku.squares[4].assign_number(2)
    NewSudoku.squares[40].assign_number(4)
    NewSudoku.squares[31].assign_number(2)
    NewSudoku.squares[31].assign_number(4)
    assert NewSudoku.squares[31].number == 0

def test_numbers_are_invalid_for_square_if_already_present_in_same_row():
    NewSudoku = Sudoku()
    NewSudoku.squares[27].assign_number(2)
    NewSudoku.squares[29].assign_number(4)
    NewSudoku.squares[35].assign_number(2)
    NewSudoku.squares[35].assign_number(4)
    assert NewSudoku.squares[35].number == 0

def test_numbers_are_invalid_for_square_if_already_present_in_same_region():
    NewSudoku = Sudoku() 
    assert NewSudoku.squares[45].possible_numbers == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    NewSudoku.squares[33].assign_number(2)
    NewSudoku.squares[52].assign_number(4)
    NewSudoku.squares[44].assign_number(2)
    NewSudoku.squares[44].assign_number(4)
    assert NewSudoku.squares[44].number == 0


retcode = pytest.main(["-x", __file__])
