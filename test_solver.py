import pytest
from sudoku import *
import solver

# if there is only one possible number for a particular square,
# then it is the right correct number for that square. 
def test_naked_single():
    Ns = Sudoku()
    for n in range(1, 4):
        Ns.rows[0][n].assign_number(n)
    for n in range(4, 7):
        Ns.columns[0][n].assign_number(n)
    for n in range(7,9):
        Ns.regions[0][n].assign_number(n)
    solver.naked_single(Ns)
    assert Ns.squares[0].number == 9

# if for a column, row or region, there is only one possibilty in which square
# a particular number could be entered, then it is the right number for that square.
# Test only covers the case, when the hidden single is deduced from the possible numbers
# in a region, so cutting out the parts checking the rows and the columns wont affect the 
# results of the test, but it also should not affect the functionality in a real world scenario.. hopefully..
def test_hidden_single():
    Ns = Sudoku()
    Ns.rows[1][0].assign_number(1)
    Ns.rows[1][2].assign_number(3)
    Ns.rows[0][3].assign_number(2)
    Ns.rows[2][8].assign_number(2)
    solver.hidden_single(Ns)
    assert Ns.rows[1][1].number == 2


retcode = pytest.main(["-x", __file__])
