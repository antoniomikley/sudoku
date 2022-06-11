# Sudoku
# Implemented Features
1. Capability to solve all sudoku puzzles and get all possible solutions if there are multiple
2. Solve a Sudoku puzzle with actual techniques and not through brute force. Currently implemented solving technique are:
  - Naked Single
  - Hidden Single
  - Naked Pair
  - Hidden Pair
  - Locked Candidates
  - Naked Triplets/Quads
  - Hidden Triplets/Quads
  - X-Wing
3. A clumsy way to input your own sudoku puzzles into a terminal and have them solved

# Currently missing features
1. Some techniques to solve more advanced sudoku puzzles:
  - Swordfish
  - XY-Wing
  - XYZ-Wing
  - Coloring
  - Forcing Chain
  - Nishio
2. Ability to generate sudoku puzzles of varrying difficulty
3. A nice GUI

There are short explanations for currently impelmented solving tehniques in the solver test file.
Information about these techniques I got from [here](https://sudoku9x9.com/sudoku_solving_techniques_9x9.html).
To use the cli run main.py in the terminal. Requires Python3 (obviously).
The tests require pyTest.
