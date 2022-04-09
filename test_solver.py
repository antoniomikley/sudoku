import pytest
from sudoku import *
import solver

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

retcode = pytest.main(["-x", __file__])
