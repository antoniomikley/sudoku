import pytest
from sudoku import *
from solver import *

def test_naked_single():
    NS = Sudoku()
    for n in range(1, 4):
        NS.rows[0][n].assign_number(n)
    for n in range(4, 7):
        NS.columns[0][n].assign_number(n)
    for n in range(7,9):
        NS.regions[0][n].assign_number(n)
    NS.solve_naked_single()
    assert NS.squares[0].number == 9

retcode = pytest.main(["-x", __file__])
